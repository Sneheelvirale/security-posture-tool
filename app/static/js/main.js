/**
 * SecurePosture — Main JavaScript
 * General utilities and UI interactions.
 */

// === Flash Message Auto-Dismiss ===
document.addEventListener('DOMContentLoaded', () => {
  const flashContainer = document.querySelector('.flash-container');
  if (flashContainer) {
    const alerts = flashContainer.querySelectorAll('.alert');
    alerts.forEach(alert => {
      setTimeout(() => {
        alert.classList.add('fade-out');
        setTimeout(() => alert.remove(), 400);
      }, 5000);

      // Manual close
      const closeBtn = alert.querySelector('.btn-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          alert.classList.add('fade-out');
          setTimeout(() => alert.remove(), 400);
        });
      }
    });
  }
});

// === Confirm Dialog for Destructive Actions ===
function confirmAction(message = 'Are you sure? This action cannot be undone.') {
  return confirm(message);
}

// Attach to all elements with data-confirm
document.addEventListener('DOMContentLoaded', () => {
  const confirmLinks = document.querySelectorAll('[data-confirm]');
  confirmLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const msg = link.getAttribute('data-confirm') || 'Are you sure?';
      if (!confirmAction(msg)) {
        e.preventDefault();
      }
    });
  });
});

// === Print Report Function ===
function printReport() {
  window.print();
}

// === Table Sorting Utility ===
function initTableSort() {
  const sortableTables = document.querySelectorAll('.table-sortable');

  sortableTables.forEach(table => {
    const headers = table.querySelectorAll('thead th.sortable');
    const tbody = table.querySelector('tbody');

    if (!tbody) return;

    headers.forEach((header, index) => {
      header.addEventListener('click', () => {
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isAsc = header.classList.contains('asc');

        // Clear all sorting indicators
        headers.forEach(h => h.classList.remove('asc', 'desc'));

        // Set new direction
        header.classList.toggle('asc', !isAsc);
        header.classList.toggle('desc', isAsc);

        // Sort rows
        rows.sort((a, b) => {
          const aText = a.children[index]?.textContent.trim() || '';
          const bText = b.children[index]?.textContent.trim() || '';

          // Try numeric comparison first
          const aNum = parseFloat(aText);
          const bNum = parseFloat(bText);

          if (!isNaN(aNum) && !isNaN(bNum)) {
            return isAsc ? bNum - aNum : aNum - bNum;
          }

          // Fall back to string comparison
          return isAsc
            ? bText.localeCompare(aText)
            : aText.localeCompare(bText);
        });

        // Reattach rows
        rows.forEach(row => tbody.appendChild(row));
      });
    });
  });
}

document.addEventListener('DOMContentLoaded', initTableSort);

// === Sidebar Toggle (Mobile) ===
document.addEventListener('DOMContentLoaded', () => {
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  const overlay = document.getElementById('sidebarOverlay');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('show');

      // Create/toggle overlay
      if (!overlay) {
        const newOverlay = document.createElement('div');
        newOverlay.id = 'sidebarOverlay';
        newOverlay.style.cssText = `
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0,0,0,0.5);
          z-index: 99;
          display: none;
        `;
        document.body.appendChild(newOverlay);

        newOverlay.addEventListener('click', () => {
          sidebar.classList.remove('show');
          newOverlay.style.display = 'none';
        });
      }

      const currentOverlay = document.getElementById('sidebarOverlay');
      if (currentOverlay) {
        currentOverlay.style.display = sidebar.classList.contains('show') ? 'block' : 'none';
      }
    });
  }
});

// === Form Validation Helpers ===
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return false;

  let valid = true;
  const requiredFields = form.querySelectorAll('[required]');

  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.classList.add('is-invalid');
      valid = false;

      // Add error message if not exists
      if (!field.nextElementSibling?.classList.contains('invalid-feedback')) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = 'This field is required.';
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
      }
    } else {
      field.classList.remove('is-invalid');
    }
  });

  return valid;
}

// Real-time validation on blur
document.addEventListener('DOMContentLoaded', () => {
  const requiredInputs = document.querySelectorAll('input[required], textarea[required], select[required]');

  requiredInputs.forEach(input => {
    input.addEventListener('blur', () => {
      if (!input.value.trim()) {
        input.classList.add('is-invalid');
      } else {
        input.classList.remove('is-invalid');
      }
    });

    input.addEventListener('input', () => {
      if (input.value.trim()) {
        input.classList.remove('is-invalid');
      }
    });
  });
});

// === Score Badge Helper ===
function getScoreBadgeHTML(score) {
  const level = Math.min(5, Math.max(0, Math.round(score)));
  return `<span class="score-badge score-${level}">${score.toFixed(1)}</span>`;
}

function getScoreLabelHTML(score, showLabel = true) {
  const level = Math.min(5, Math.max(0, Math.round(score)));
  const labels = ['Not Impl.', 'Initial', 'Developing', 'Defined', 'Managed', 'Optimising'];
  return showLabel
    ? `<span class="score-label score-${level}">${labels[level]}</span>`
    : `<span class="score-label score-${level}">${score.toFixed(1)}</span>`;
}

// === Evidence Badge Helper ===
function getEvidenceBadgeHTML(status) {
  const statusMap = {
    'none': 'evidence-none',
    'partial': 'evidence-partial',
    'full': 'evidence-full'
  };
  const labelMap = {
    'none': 'No Evidence',
    'partial': 'Partial',
    'full': 'Full'
  };
  const className = statusMap[status] || 'evidence-none';
  const label = labelMap[status] || status;
  return `<span class="evidence-badge ${className}">${label}</span>`;
}

// === Loading Spinner ===
function showSpinner(targetId) {
  const target = document.getElementById(targetId);
  if (!target) return;

  target.innerHTML = `
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  `;
}

// === Toast Notification (Alternative to Flash) ===
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `alert alert-${type} alert-dismissible fade show`;
  toast.setAttribute('role', 'alert');
  toast.innerHTML = `
    ${message}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
  `;

  let container = document.querySelector('.flash-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'flash-container';
    document.body.appendChild(container);
  }

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 400);
  }, 5000);
}

// === Keyboard Shortcuts ===
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + P on report page = print
  if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
    if (document.querySelector('.report-page')) {
      e.preventDefault();
      printReport();
    }
  }

  // Escape = close sidebar on mobile
  if (e.key === 'Escape') {
    const sidebar = document.querySelector('.sidebar.show');
    const overlay = document.getElementById('sidebarOverlay');
    if (sidebar) {
      sidebar.classList.remove('show');
      if (overlay) overlay.style.display = 'none';
    }
  }
});

// === Export helpers to global scope ===
window.SecurePosture = {
  confirmAction,
  printReport,
  validateForm,
  getScoreBadgeHTML,
  getScoreLabelHTML,
  getEvidenceBadgeHTML,
  showSpinner,
  showToast,
  initTableSort,
};
