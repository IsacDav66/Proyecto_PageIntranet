document.addEventListener('DOMContentLoaded', function() {
    const numBubbles = 20; // Número de burbujas
    const colors = ['#66c2ff', '#007bff', '#ff9933', '#ff6666', '#cc99ff']; // Colores degradados

    // Generar burbujas aleatorias
    for (let i = 0; i < numBubbles; i++) {
        createBubble();
    }

    // Función para crear burbujas
    function createBubble() {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        bubble.style.width = randomSize() + 'px'; // Tamaño aleatorio
        bubble.style.height = bubble.style.width;
        bubble.style.background = randomColor(); // Color aleatorio
        bubble.style.top = randomPosition() + '%'; // Posición aleatoria en vertical
        bubble.style.left = randomPosition() + '%'; // Posición aleatoria en horizontal

        document.body.appendChild(bubble);
    }

    // Función para generar tamaño aleatorio entre 40 y 120px
    function randomSize() {
        return Math.floor(Math.random() * (120 - 40 + 1)) + 40;
    }

    // Función para generar posición aleatoria entre 0 y 100%
    function randomPosition() {
        return Math.random() * 100;
    }

    // Función para elegir color aleatorio de la lista
    function randomColor() {
        return colors[Math.floor(Math.random() * colors.length)];
    }
});
