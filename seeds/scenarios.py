"""
Seeded assessment scenarios for the three fictional organisations.
Each scenario provides pre-built assessment data for validation testing.
"""


def get_seeded_scenarios():
    """
    Return realistic pre-seeded assessment data for each sample organisation.

    Each scenario includes:
      - org_name: matches a sample organisation
      - responses: list of (control_ref, maturity_score, evidence_status, evidence_description, notes)

    maturity_score: 0-5 (0=not implemented, 5=optimising)
    evidence_status: 'none', 'partial', 'full'
    """
    return [
        # ── Maple Leaf Bakery ── mostly low maturity ───────────────────
        {
            "org_name": "Maple Leaf Bakery",
            "responses": [
                # Identify
                ("ID.AM-1", 1, "partial", "Spreadsheet lists POS terminals and office PC, but no Wi-Fi router details.", "Asset tracking ad-hoc."),
                ("ID.AM-2", 0, "none", "", "No software inventory exists."),
                ("ID.AM-3", 0, "none", "", "No data flow diagram."),
                ("ID.AM-4", 1, "partial", "Email provider and POS vendor documented in a notebook.", "Informal tracking."),
                ("ID.BE-1", 1, "partial", "Owner knows supplier (POS vendor) and customers, not formally documented.", ""),
                ("ID.BE-2", 1, "partial", "Owner aware bakery is non-critical infrastructure.", ""),
                ("ID.GV-1", 0, "none", "", "No written security policy."),
                ("ID.GV-2", 0, "none", "", "No assigned security roles."),
                ("ID.RA-1", 0, "none", "", "No vulnerability scanning."),
                ("ID.RM-1", 0, "none", "", "No formal risk register."),
                # Protect
                ("PR.AC-1", 2, "partial", "Each employee has their own POS login. Office PC shared with one password.", "Partial identity management."),
                ("PR.AC-2", 2, "full", "Office locked after hours, key access only.", "Basic physical security in place."),
                ("PR.AC-3", 0, "none", "", "No remote access to systems."),
                ("PR.AC-4", 1, "partial", "POS accounts have basic role separation (cashier vs manager).", "Least privilege not enforced on office PC."),
                ("PR.AC-5", 0, "none", "", "No MFA enabled anywhere."),
                ("PR.AT-1", 0, "none", "", "No formal security training."),
                ("PR.AT-2", 0, "none", "", "No privileged user training (none identified)."),
                ("PR.DS-1", 0, "none", "", "No disk encryption on office PC."),
                ("PR.DS-2", 1, "partial", "POS uses HTTPS to payment processor. Email unencrypted.", ""),
                ("PR.IP-1", 0, "none", "", "No configuration baselines."),
                ("PR.IP-4", 1, "partial", "POS vendor handles backups of transaction data. No backup of office files.", "Dependent on vendor."),
                ("PR.MA-1", 1, "partial", "POS vendor performs maintenance. Not logged.", ""),
                # Detect
                ("DE.AE-1", 0, "none", "", "No network baseline."),
                ("DE.AE-2", 0, "none", "", "No event analysis capability."),
                ("DE.AE-3", 0, "none", "", "No log aggregation."),
                ("DE.CM-1", 0, "none", "", "No network monitoring."),
                ("DE.CM-2", 0, "none", "", "No cameras or access logs."),
                ("DE.CM-3", 0, "none", "", "No user activity monitoring."),
                ("DE.CM-4", 1, "partial", "Windows Defender enabled on office PC, but not managed.", ""),
                ("DE.DP-1", 0, "none", "", "No detection roles assigned."),
                ("DE.DP-4", 0, "none", "", "No event communication process."),
                # Respond
                ("RS.RP-1", 0, "none", "", "No incident response plan."),
                ("RS.CO-1", 0, "none", "", "No defined response roles."),
                ("RS.CO-2", 1, "partial", "Staff told to call owner if 'something breaks'.", "Informal reporting."),
                ("RS.CO-3", 0, "none", "", "No information sharing agreements."),
                ("RS.AN-1", 0, "none", "", "No alert investigation process."),
                ("RS.AN-2", 0, "none", "", "No impact assessment capability."),
                ("RS.MI-1", 0, "none", "", "No containment procedures."),
                ("RS.IM-1", 0, "none", "", "No lessons learned process."),
                # Recover
                ("RC.RP-1", 1, "partial", "POS vendor can restore POS from their backup. No plan for office PC.", ""),
                ("RC.RP-2", 0, "none", "", "No plan update process."),
                ("RC.IM-1", 0, "none", "", "No recovery metrics tracked."),
                ("RC.IM-2", 0, "none", "", "No recovery strategy review."),
                ("RC.CO-1", 0, "none", "", "No PR plan."),
                ("RC.CO-2", 0, "none", "", "No reputation recovery plan."),
            ],
        },
        # ── TechStart Solutions ── mixed maturity ──────────────────────
        {
            "org_name": "TechStart Solutions",
            "responses": [
                # Identify
                ("ID.AM-1", 3, "full", "AWS inventory tracked via Terraform state and auto-discovery scripts.", "Good hardware asset visibility."),
                ("ID.AM-2", 3, "full", "Package managers and SaaS subscriptions listed in internal wiki.", ""),
                ("ID.AM-3", 2, "partial", "Architecture diagram exists but not kept current.", ""),
                ("ID.AM-4", 3, "full", "All third-party APIs documented in developer portal.", ""),
                ("ID.BE-1", 2, "partial", "Supply chain documented in sales docs but not formally reviewed.", ""),
                ("ID.BE-2", 2, "full", "Business continuity plan identifies critical SaaS product.", ""),
                ("ID.GV-1", 2, "partial", "Security policy exists but not recently reviewed or communicated.", "Needs refresh."),
                ("ID.GV-2", 3, "full", "CTO owns security, devops lead handles infrastructure. Documented in wiki.", ""),
                ("ID.RA-1", 3, "full", "Automated vulnerability scans via AWS Inspector and Dependabot.", ""),
                ("ID.RM-1", 2, "partial", "Risk register exists but not reviewed regularly.", ""),
                # Protect
                ("PR.AC-1", 4, "full", "SSO (Okta) with unique credentials per user. Centrally managed.", "Strong identity management."),
                ("PR.AC-2", 1, "partial", "Remote-first; no physical office. Home office security not verified.", ""),
                ("PR.AC-3", 4, "full", "VPN required for production access, MFA enforced.", ""),
                ("PR.AC-4", 3, "full", "IAM roles follow least privilege. Reviewed quarterly.", ""),
                ("PR.AC-5", 4, "full", "MFA required on AWS, GitHub, Slack, and all SaaS tools.", ""),
                ("PR.AT-1", 2, "partial", "Onboarding security training exists but no ongoing refreshers.", ""),
                ("PR.AT-2", 3, "full", "Admins receive additional AWS security training.", ""),
                ("PR.DS-1", 3, "full", "RDS encryption enabled, S3 buckets encrypted. Laptop encryption enforced via MDM.", ""),
                ("PR.DS-2", 4, "full", "TLS everywhere. API Gateway enforces HTTPS.", ""),
                ("PR.IP-1", 3, "full", "Infrastructure-as-code (Terraform) defines config baselines.", ""),
                ("PR.IP-4", 4, "full", "Automated daily backups to S3 with versioning. Restore tested quarterly.", ""),
                ("PR.MA-1", 3, "full", "Patch management automated via AWS Systems Manager. Logged.", ""),
                # Detect
                ("DE.AE-1", 2, "partial", "CloudWatch tracks usage but no formal baseline.", ""),
                ("DE.AE-2", 2, "partial", "Some alerts reviewed, but no formal analysis workflow.", ""),
                ("DE.AE-3", 3, "full", "CloudWatch Logs aggregates VPC flow logs, app logs, and WAF logs.", ""),
                ("DE.CM-1", 3, "full", "AWS GuardDuty enabled for threat detection.", ""),
                ("DE.CM-2", 0, "none", "", "No physical monitoring (remote-first)."),
                ("DE.CM-3", 2, "partial", "CloudTrail logs admin actions. No user endpoint monitoring.", ""),
                ("DE.CM-4", 3, "full", "CrowdStrike deployed on all laptops.", ""),
                ("DE.DP-1", 3, "full", "DevOps lead reviews GuardDuty alerts daily. Escalation to CTO documented.", ""),
                ("DE.DP-4", 3, "full", "Alerts posted to #security Slack channel.", ""),
                # Respond
                ("RS.RP-1", 2, "partial", "Incident runbook exists but not tested.", "Needs tabletop exercise."),
                ("RS.CO-1", 2, "partial", "Roles defined in runbook but not trained.", ""),
                ("RS.CO-2", 3, "full", "Incidents reported via PagerDuty and Slack.", ""),
                ("RS.CO-3", 2, "partial", "Customer communication plan exists but not validated.", ""),
                ("RS.AN-1", 3, "full", "PagerDuty alerts triaged within 4 hours.", ""),
                ("RS.AN-2", 2, "partial", "Impact assessed informally, no structured checklist.", ""),
                ("RS.MI-1", 2, "partial", "Can isolate EC2 instances via security groups. No formal playbook.", ""),
                ("RS.IM-1", 2, "partial", "Post-incident Slack threads captured but not formalised.", ""),
                # Recover
                ("RC.RP-1", 2, "partial", "Restore procedures exist for RDS and S3. Not tested end-to-end.", "Needs full DR drill."),
                ("RC.RP-2", 1, "partial", "Plan updated ad-hoc after incidents but no formal review cycle.", ""),
                ("RC.IM-1", 1, "partial", "RTO/RPO defined but not measured after tests.", ""),
                ("RC.IM-2", 1, "partial", "Recovery strategy not revisited since launch.", ""),
                ("RC.CO-1", 2, "partial", "PR template drafted. No designated spokesperson.", ""),
                ("RC.CO-2", 1, "partial", "No reputation recovery plan beyond apology emails.", ""),
            ],
        },
        # ── Greenfield Medical Clinic ── moderate maturity ─────────────
        {
            "org_name": "Greenfield Medical Clinic",
            "responses": [
                # Identify
                ("ID.AM-1", 2, "partial", "IT contractor maintains inventory of desktops, server, and medical devices.", "Inventory exists but not live."),
                ("ID.AM-2", 2, "partial", "EHR system and office productivity software documented.", "Some shadow IT unknown."),
                ("ID.AM-3", 1, "partial", "EHR vendor provided a high-level data flow diagram.", "Not tailored to clinic's environment."),
                ("ID.AM-4", 3, "full", "All external systems (EHR cloud, lab integration, billing) listed in vendor matrix.", ""),
                ("ID.BE-1", 2, "full", "Clinic role in healthcare delivery chain documented for accreditation.", ""),
                ("ID.BE-2", 2, "full", "Aware clinic handles protected health information (PHI).", ""),
                ("ID.GV-1", 3, "full", "HIPAA-aligned security policy distributed to all staff. Reviewed annually.", "Strong policy foundation."),
                ("ID.GV-2", 3, "full", "Practice manager is security officer. IT contractor handles technical controls.", ""),
                ("ID.RA-1", 2, "partial", "Annual risk assessment required by HIPAA but informal.", "Needs structured process."),
                ("ID.RM-1", 2, "full", "Risk register maintained for compliance. Reviewed at board meetings.", ""),
                # Protect
                ("PR.AC-1", 3, "full", "Unique EHR logins per user. Disabled promptly when staff leave.", "Good credential management."),
                ("PR.AC-2", 3, "full", "Server room locked. Badge access to clinical areas logged.", ""),
                ("PR.AC-3", 2, "partial", "Remote EHR access via VPN. MFA not yet enabled.", "MFA planned."),
                ("PR.AC-4", 3, "full", "Role-based access in EHR. Doctors, nurses, reception have different permissions.", ""),
                ("PR.AC-5", 1, "partial", "MFA enabled for IT contractor admin access only.", "Not rolled out to all users."),
                ("PR.AT-1", 3, "full", "Annual HIPAA training mandatory for all staff. Attendance tracked.", ""),
                ("PR.AT-2", 2, "full", "IT contractor trained on EHR security settings.", ""),
                ("PR.DS-1", 3, "full", "EHR database encrypted by vendor. Workstation disk encryption deployed.", ""),
                ("PR.DS-2", 3, "full", "EHR accessed via HTTPS. VPN uses TLS.", ""),
                ("PR.IP-1", 2, "partial", "Workstation builds follow a checklist but not version-controlled.", ""),
                ("PR.IP-4", 3, "full", "EHR vendor performs nightly backups. Clinic backs up local files weekly. Restore tested.", ""),
                ("PR.MA-1", 3, "full", "IT contractor logs all maintenance. Patch schedule monthly.", ""),
                # Detect
                ("DE.AE-1", 1, "none", "", "No network baseline established."),
                ("DE.AE-2", 1, "partial", "IT contractor reviews alerts but no formal analysis.", ""),
                ("DE.AE-3", 2, "partial", "Firewall logs collected. EHR audit logs viewed in vendor portal, not aggregated.", ""),
                ("DE.CM-1", 2, "partial", "Firewall monitors traffic. No IDS/IPS.", "Basic monitoring only."),
                ("DE.CM-2", 3, "full", "Security cameras at entrances. Access logs for server room.", ""),
                ("DE.CM-3", 2, "partial", "EHR tracks user logins and access to patient records. Spot-checked.", ""),
                ("DE.CM-4", 3, "full", "Managed antivirus on all workstations.", ""),
                ("DE.DP-1", 2, "full", "IT contractor responsible for alert review. Escalation to practice manager.", ""),
                ("DE.DP-4", 2, "partial", "IT contractor emails practice manager when issues found.", "No formal incident channel."),
                # Respond
                ("RS.RP-1", 2, "partial", "Breach notification plan exists (HIPAA requirement). Not tested.", ""),
                ("RS.CO-1", 2, "full", "Staff trained to report suspected breaches to practice manager immediately.", ""),
                ("RS.CO-2", 3, "full", "Incident reporting form on intranet. HIPAA breach log maintained.", ""),
                ("RS.CO-3", 3, "full", "Breach notification templates prepared. Legal counsel on retainer.", ""),
                ("RS.AN-1", 2, "partial", "IT contractor investigates incidents reactively. No SLA.", ""),
                ("RS.AN-2", 2, "partial", "Impact assessed for patient data exposure. Other impacts less clear.", ""),
                ("RS.MI-1", 2, "partial", "IT contractor can disconnect devices. No formal containment playbook.", ""),
                ("RS.IM-1", 2, "partial", "Lessons learned captured in breach log but not systematically applied.", ""),
                # Recover
                ("RC.RP-1", 2, "partial", "EHR recovery plan provided by vendor. Clinic has no local recovery plan for downtime.", "Vendor-dependent."),
                ("RC.RP-2", 1, "partial", "Plan reviewed after EHR upgrades but not regularly.", ""),
                ("RC.IM-1", 1, "partial", "No recovery metrics defined.", ""),
                ("RC.IM-2", 1, "partial", "Recovery strategy not updated since EHR migration.", ""),
                ("RC.CO-1", 2, "full", "Breach notification templates prepared for patients and regulator.", ""),
                ("RC.CO-2", 1, "partial", "No formal reputation recovery plan beyond notification.", ""),
            ],
        },
    ]
