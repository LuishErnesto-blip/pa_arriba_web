document.addEventListener('DOMContentLoaded', function () {
  // Scope everything to the form to avoid collisions with other pages/components
  const form = document.querySelector('.termometro-form');
  if (!form) return; // If the form isn't present, do nothing

  const steps = form.querySelectorAll('.wizard-step');
  const progress = form.querySelector('.progress');
  const successModal = document.getElementById('successModal');
  const closeModalBtn = document.getElementById('closeModal');
  const summaryStep = document.querySelector('.summary-step'); // summary lives outside .wizard-step
  const summaryText = document.getElementById('summaryText');
  const summaryScore = document.getElementById('summaryScore');
  const goToStep5Btn = document.getElementById('goToStep5');

  // Defensive checks
  if (!steps.length || !progress || !summaryStep || !summaryText || !summaryScore) {
    console.warn('Termómetro: faltan elementos requeridos en el DOM.');
    return;
  }

  let currentStep = 0; // 0-based
  let answers = [];
  let scores = [];

  // Helper: show step and update progress
  function showStep(index) {
    steps.forEach((step, i) => {
      step.classList.toggle('active', i === index);
      if (i === index) step.style.animation = 'fadeSlideIn 1s ease forwards';
    });

    // Hide summary unless explicitly asked
    summaryStep.classList.remove('active');
    summaryStep.style.display = 'none';

    // Progress: 4 question steps; summary considered 80%, step 5 considered 100%
    const pct = Math.min(((index + 1) / 4) * 100, 100);
    progress.style.width = `${pct}%`;
  }

  // Helper: show summary
  function showSummary() {
    const validScores = scores.slice(0, 4).filter(s => typeof s === 'number');
    if (!validScores.length) return;

    const totalScore = validScores.reduce((a, b) => a + b, 0);
    const avgScore = totalScore / validScores.length;

    let mensajeUrgencia = '';
    let alertClass = '';

    if (avgScore >= 4) {
      mensajeUrgencia = 'Tu negocio está sólido, pero aún puedes optimizar con nuestras herramientas digitales.';
      alertClass = 'alert-green';
    } else if (avgScore >= 2) {
      mensajeUrgencia = 'Tu negocio está en riesgo medio, necesitas apoyo estratégico para crecer.';
      alertClass = 'alert-yellow';
    } else {
      mensajeUrgencia = 'Tu negocio está en riesgo alto, es urgente implementar soluciones digitales.';
      alertClass = 'alert-red';
    }

    summaryText.innerHTML = `
      Respondiste: <br>
      • Finanzas: ${answers[0] || 'N/A'} <br>
      • Avance sin ti: ${answers[1] || 'N/A'} <br>
      • Decisiones: ${answers[2] || 'N/A'} <br>
      • Tecnología: ${answers[3] || 'N/A'}
    `;
    summaryScore.innerHTML = `
      <div class="${alertClass}" style="margin-top: 1rem;">
        <strong>Puntaje promedio:</strong> ${avgScore.toFixed(1)} / 5 <br>${mensajeUrgencia}
      </div>
    `;

    // Hide question steps
    steps.forEach(step => step.classList.remove('active'));
    // Show summary
    summaryStep.classList.add('active');
    summaryStep.style.display = 'block';
    progress.style.width = '80%';
    currentStep = 'summary';
  }

  // Register clicks on options
  form.querySelectorAll('.wizard-options button').forEach(button => {
    button.addEventListener('click', () => {
      const stepEl = button.closest('.wizard-step');
      if (!stepEl) return;

      // Use data-step if present, otherwise infer from DOM order
      const ds = stepEl.getAttribute('data-step');
      const stepIndex = ds ? parseInt(ds, 10) - 1 : Array.from(steps).indexOf(stepEl);
      if (isNaN(stepIndex) || stepIndex < 0) return;

      const fieldName = stepEl.getAttribute('data-name') || `step_${stepIndex + 1}`;
      const value = button.getAttribute('data-value') || button.textContent.trim();
      const score = parseInt(button.getAttribute('data-score') || '0', 10);

      // Save answer and score
      answers[stepIndex] = value;
      scores[stepIndex] = score;

      // Create/update hidden input
      const existingInput = form.querySelector(`input[name='respuesta_${fieldName}']`);
      if (existingInput) existingInput.remove();
      const hidden = document.createElement('input');
      hidden.type = 'hidden';
      hidden.name = `respuesta_${fieldName}`;
      hidden.value = value;
      form.appendChild(hidden);

      // Next step or summary
      if (stepIndex < 3) {
        currentStep = stepIndex + 1;
        showStep(currentStep);
      } else {
        showSummary();
      }
    });
  });

  // Continue to step 5
  if (goToStep5Btn) {
    goToStep5Btn.addEventListener('click', () => {
      summaryStep.classList.remove('active');
      summaryStep.style.display = 'none';
      // Step 5 is index 4 (data-step="5")
      currentStep = 4;
      showStep(currentStep);
      progress.style.width = '100%';
    });
  }

  // Submit with validation and modal
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const step5 = form.querySelector('.wizard-step[data-step="5"]');
    const requiredFields = step5 ? step5.querySelectorAll('[required]') : [];
    let valid = true;
    requiredFields.forEach(f => {
      if (!f.value || (f.tagName === 'SELECT' && f.value === '')) valid = false;
    });

    const inputContainer = step5 ? step5.querySelector('.wizard-inputs') : null;
    if (inputContainer) {
      let errorDiv = document.getElementById('validationError');
      if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.id = 'validationError';
        errorDiv.className = 'alert-red mt-4 mb-2';
        errorDiv.style.fontWeight = 'normal';
        errorDiv.style.marginTop = '1rem';
        errorDiv.style.marginBottom = '1rem';
        inputContainer.parentNode.insertBefore(errorDiv, inputContainer.nextSibling);
      }
      if (!valid) {
        errorDiv.style.display = 'block';
        errorDiv.textContent = '🛑 Por favor, completa todos tus datos antes de enviar.';
        return;
      } else {
        errorDiv.style.display = 'none';
      }
    }

    // Show success modal if present, otherwise submit directly
    if (successModal) {
      successModal.style.display = 'flex';
      const icon = successModal.querySelector('.modal-icon');
      if (icon) icon.style.animation = 'zoomIn 1s ease forwards';

      if (closeModalBtn) {
        closeModalBtn.onclick = () => {
          successModal.style.display = 'none';
          form.submit();
        };
      }

      setTimeout(() => {
        successModal.style.display = 'none';
        form.submit();
      }, 30000);
    } else {
      form.submit();
    }
  });

  // Initialize
  showStep(currentStep);
});
