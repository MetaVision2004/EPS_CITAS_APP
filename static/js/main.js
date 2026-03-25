// Auto-ocultar alertas después de 5 segundos
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity .5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Fecha mínima: hoy
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        if (!input.value) input.setAttribute('min', today);
    });

    const DIRECCIONES_EPS = {
        'Sura': 'Calle 50 # 45-20, Medellín',
        'Sanitas': 'Calle 100 # 11-60, Bogotá',
        'Nueva EPS': 'Carrera 45 # 95-12, Bogotá',
        'Compensar': 'Avenida 68 # 49-47, Bogotá',
        'Salud Total': 'Calle 10 # 50-30, Cali',
        'Coosalud': 'Carrera 20 # 30-15, Cartagena',
        'Famisanar': 'Calle 72 # 10-03, Bogotá',
        'Cafesalud': 'Avenida El Dorado # 68-15, Bogotá',
        'Medimás': 'Calle 26 # 69-76, Bogotá',
        'Coomeva': 'Calle 13 # 58-35, Cali',
        'Mutual Ser': 'Barrio Getsemaní, Cartagena'
    };

    const epsSelect = document.getElementById('eps');
    const direccionInput = document.getElementById('direccion_eps');
    const documentoInput = document.getElementById('documento');

    if (epsSelect && direccionInput) {
        epsSelect.addEventListener('change', () => {
            const epsValue = epsSelect.value;
            direccionInput.value = DIRECCIONES_EPS[epsValue] || '';
        });
    }

    if (documentoInput && epsSelect && direccionInput) {
        documentoInput.addEventListener('blur', () => {
            const documento = documentoInput.value.trim();
            if (!documento) return;

            fetch(`/api/direccion_eps/${encodeURIComponent(documento)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.eps) {
                        if (DIRECCIONES_EPS[data.eps]) {
                            epsSelect.value = data.eps;
                            direccionInput.value = DIRECCIONES_EPS[data.eps];
                        } else {
                            direccionInput.value = data.direccion || '';
                        }
                    }
                })
                .catch(err => {
                    console.error('Error buscando EPS/dirección:', err);
                });
        });
    }
});
