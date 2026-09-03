"""Seed data loader for populating database with NIST controls and sample organisations."""
from seeds.controls import get_nist_controls
from seeds.organisations import get_sample_organisations
from seeds.scenarios import get_seeded_scenarios
from app.models import Control, Organisation, User, Assessment, AssessmentResponse
from datetime import datetime


def seed_all(db):
    """Seed all data: controls, organisations, and sample assessments."""

    # 1. Seed NIST CSF Controls
    print("Seeding NIST CSF controls...")
    controls_data = get_nist_controls()
    controls_map = {}

    for control_data in controls_data:
        control = Control.query.filter_by(control_ref=control_data['control_ref']).first()
        if not control:
            control = Control(control_ref=control_data['control_ref'])
            db.session.add(control)

        control.function = control_data['function']
        control.category = control_data['category']
        control.title = control_data['title']
        control.description = control_data['description']
        control.guidance = control_data['guidance']
        control.effort_band = control_data['effort_band']
        controls_map[control_data['control_ref']] = control

    db.session.commit()
    print(f"✓ Loaded {len(controls_data)} NIST CSF controls")

    # 2. Create default admin user if none exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@secureposture.local',
            role='admin'
        )
        admin.set_password('admin123')  # Change in production!
        db.session.add(admin)
        db.session.commit()
        print(f"✓ Created default admin user (username: admin, password: admin123)")

    # 3. Seed sample organisations
    print("Seeding sample organisations...")
    orgs_data = get_sample_organisations()
    orgs_map = {}

    for org_data in orgs_data:
        org = Organisation.query.filter_by(name=org_data['name']).first()
        if not org:
            org = Organisation(name=org_data['name'], created_by=admin.id)
            db.session.add(org)

        org.industry = org_data['industry']
        org.size = org_data['size']
        org.description = org_data['description']
        orgs_map[org_data['name']] = org

    db.session.commit()
    print(f"✓ Created {len(orgs_data)} sample organisations")

    # 4. Seed pre-built assessment scenarios (optional realistic test data)
    print("Seeding sample assessment scenarios...")
    scenarios = get_seeded_scenarios()

    for scenario in scenarios:
        org = orgs_map.get(scenario['org_name'])
        if not org:
            continue

        existing_assessment = Assessment.query.filter_by(
            organisation_id=org.id,
            notes=f"Pre-seeded scenario for {org.name}",
        ).first()
        if existing_assessment:
            continue

        # Create assessment
        assessment = Assessment(
            organisation_id=org.id,
            assessor_id=admin.id,
            status='completed',
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            notes=f"Pre-seeded scenario for {org.name}"
        )
        db.session.add(assessment)
        db.session.flush()  # Get assessment.id

        # Add responses for each control. Support either tuple-based seed data or
        # dictionary-based data so older/newer scenario formats both work.
        for response_data in scenario['responses']:
            if isinstance(response_data, dict):
                control_ref = response_data['control_ref']
                maturity_score = response_data['maturity_score']
                evidence_status = response_data['evidence_status']
                evidence_description = response_data.get('evidence_description', '')
                notes = response_data.get('notes', '')
            else:
                (
                    control_ref,
                    maturity_score,
                    evidence_status,
                    evidence_description,
                    notes,
                ) = response_data

            control = controls_map.get(control_ref)
            if not control:
                continue

            response = AssessmentResponse(
                assessment_id=assessment.id,
                control_id=control.id,
                maturity_score=maturity_score,
                evidence_status=evidence_status,
                evidence_description=evidence_description,
                notes=notes
            )
            db.session.add(response)

    db.session.commit()
    print(f"✓ Created {len(scenarios)} pre-built assessment scenarios")

    print("\n✅ Database seeding complete!")
    print(f"   - {len(controls_data)} NIST controls")
    print(f"   - {len(orgs_data)} organisations")
    print(f"   - {len(scenarios)} sample assessments")
    print(f"\n   Login with: admin / admin123")
