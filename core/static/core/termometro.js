document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('.termometro-form');
  if (!form) return;

  // Referencias a elementos clave
  const allWizardSteps = document.querySelectorAll('.wizard-step');
  const summaryStep = document.querySelector('.summary-step');
  const progress = form.querySelector('.progress');
  const successModal = document.getElementById('successModal');
  const closeModalBtn = document.getElementById('closeModal');
  const summaryText = document.getElementById('summaryText');
  const summaryScore = document.getElementById('summaryScore');
  const goToStep5Btn = document.getElementById('goToStep5');
  const successMessage = document.getElementById('successMessage'); // Referencia al mensaje de carga

  const totalQuestionSteps = 4; // Pasos de preguntas (1 a 4)
  
  // Variables de estado
  let currentStep = 1; 
  const answers = {};
  const scores = {};

  // Función para mostrar un paso específico
  function showStep(stepNumber) {
    console.log(`Mostrando paso: ${stepNumber}`);

    // 1. Ocultar TODO primero
    allWizardSteps.forEach(step => {
        step.classList.remove('active');
        step.style.display = 'none'; // Forzamos ocultar
    });
    if (summaryStep) {
        summaryStep.classList.remove('active');
        summaryStep.style.display = 'none';
    }

    // 2. Mostrar el paso correspondiente
    if (stepNumber === 'summary') {
        // Mostrar Resumen
        if (summaryStep) {
            summaryStep.style.display = 'block';
            summaryStep.classList.add('active');
            summaryStep.style.animation = 'fadeSlideIn 1s ease forwards';
        }
        // Barra de progreso al 80%
        if (progress) progress.style.width = '80%';
    } else {
        // Mostrar paso numérico (1, 2, 3, 4, 5)
        // Buscamos el paso con el data-step correspondiente
        const stepToShow = document.querySelector(`.wizard-step[data-step="${stepNumber}"]`);
        if (stepToShow) {
            stepToShow.style.display = 'block';
            stepToShow.classList.add('active');
            stepToShow.style.animation = 'fadeSlideIn 1s ease forwards';
        }
        
        // Actualizar barra de progreso
        if (progress) {
            const pct = Math.min((stepNumber / 5) * 100, 100);
            progress.style.width = `${pct}%`;
        }
    }
    currentStep = stepNumber;
  }

  // Función para calcular y mostrar el resumen
  function renderSummary() {
    // Calcular puntaje promedio
    const validScores = Object.values(scores);
    const totalScore = validScores.reduce((a, b) => a + b, 0);
    const avgScore = validScores.length ? (totalScore / validScores.length) : 0;

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

    // Actualizar textos del resumen
    summaryText.innerHTML = `
      <strong>Tus Respuestas:</strong><br>
      1. Finanzas: ${answers['crece'] || '-'} <br>
      2. Operación: ${answers['avanza'] || '-'} <br>
      3. Decisiones: ${answers['mejora'] || '-'} <br>
      4. Tecnología: ${answers['reemprende'] || '-'}
    `;

    summaryScore.innerHTML = `
      <div class="${alertClass}" style="margin-top: 1rem;">
        <strong>Puntaje promedio:</strong> ${avgScore.toFixed(1)} / 5 <br>${mensajeUrgencia}
      </div>
    `;

    showStep('summary');
  }

  // MANEJO DE CLICS EN OPCIONES
  form.addEventListener('click', (e) => {
    // Verificar si el clic fue en un botón de opción
    const btn = e.target.closest('.wizard-options button');
    if (!btn) return;
    
    // Prevenir comportamiento por defecto
    e.preventDefault();

    // Identificar en qué paso estamos
    const stepEl = btn.closest('.wizard-step');
    if (!stepEl) return;

    const stepNum = parseInt(stepEl.getAttribute('data-step'), 10);
    const fieldName = stepEl.getAttribute('data-name');
    
    // Obtener datos del botón
    const value = btn.getAttribute('data-value');
    const score = parseInt(btn.getAttribute('data-score'), 10);

    // Guardar datos
    answers[fieldName] = value;
    scores[fieldName] = score;

    // Crear/Actualizar input oculto para el envío final
    const inputName = `respuesta_${fieldName}`;
    let hiddenInput = form.querySelector(`input[name="${inputName}"]`);
    if (!hiddenInput) {
        hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = inputName;
        form.appendChild(hiddenInput);
    }
    hiddenInput.value = value;

    // Lógica de Avance
    if (stepNum < totalQuestionSteps) {
        // Si es pregunta 1, 2 o 3 -> Ir a la siguiente
        showStep(stepNum + 1);
    } else {
        // Si es la pregunta 4 -> Ir al resumen
        renderSummary();
    }
  });

  // Botón "Continuar" en el resumen
  if (goToStep5Btn) {
    goToStep5Btn.addEventListener('click', (e) => {
        e.preventDefault();
        showStep(5); // Ir al paso de captura de datos
    });
  }

  // ==========================================
  // NUEVO MANEJO DEL ENVÍO (AJAX + MODAL)
  // ==========================================
  form.addEventListener('submit', function (e) {
    e.preventDefault(); // Evita recargar la página

    // Validación simple de campos del paso 5
    const step5 = document.querySelector('.wizard-step[data-step="5"]');
    const inputs = step5.querySelectorAll('input, select');
    let valid = true;

    inputs.forEach(input => {
        if (!input.value) valid = false;
    });

    if (!valid) {
        alert("Por favor, completa todos los campos de contacto.");
        return;
    }
    
    // Mostrar mensaje temporal "Enviando..." si existe en el HTML
    if (successMessage) {
        successMessage.style.display = 'block';
        successMessage.classList.add('active');
    }

    // Enviar datos en segundo plano
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        // Ocultar mensaje "Enviando..."
        if (successMessage) successMessage.style.display = 'none';

        if (response.ok) {
            // ÉXITO: Mostrar el Modal
            if (successModal) {
                // Usamos 'flex' para que CSS centre el contenido
                successModal.style.display = 'flex';
                // *** GOOGLE ADS CONVERSION ***
                if (typeof gtag === 'function') {
                    gtag('event', 'conversion', {'send_to': 'AW-17785566071/du3NCKvupc4bEPfm6KBC'});
                }
                // *****************************
            }
        } else {
            alert("Hubo un problema al guardar tu diagnóstico. Por favor intenta de nuevo.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (successMessage) successMessage.style.display = 'none';
        alert("Error de conexión. Revisa tu internet.");
    });
  });

  // Botón cerrar dentro del Modal
  if (closeModalBtn) {
      closeModalBtn.addEventListener('click', function() {
          // Al cerrar, recargamos o enviamos al inicio
          window.location.href = "/"; 
      });
  }

  // Inicializar: Ocultar todo excepto el paso 1
  showStep(1);
});