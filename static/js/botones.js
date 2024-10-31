
    // Función para mostrar un formulario y ocultar los demás
    function mostrarFormulario(id) {
        var formularios = document.querySelectorAll('form'); // Obtener todos los formularios
        formularios.forEach(function(formulario) {
            if (formulario.id === id) {
                formulario.style.display = 'block'; // Mostrar el formulario con el ID dado
            } else {
                formulario.style.display = 'none'; // Ocultar los demás formularios
            }
        });
    }
    document.getElementById('agregar').addEventListener('click', function() {
        mostrarFormulario('form1');
    });

    document.getElementById('limpiartabla').addEventListener('click', function() {
        mostrarFormulario('form2');
    });

    document.getElementById('limpiar').addEventListener('click', function() {
        mostrarFormulario('form3');
    });
