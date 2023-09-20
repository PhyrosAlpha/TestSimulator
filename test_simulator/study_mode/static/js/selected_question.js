console.log('script iniciado');

let button = document.querySelector('#show-answers');
button.addEventListener('click', function() {
    let answers = document.querySelectorAll('.question-correct');
    answers.forEach(function(answer) {
        answer.classList.toggle('show-answer');
    });

    if(button.classList.contains('btn-primary')) {
        button.classList.remove('btn-primary');
        button.classList.add('btn-secondary');
        button.innerHTML = 'Ocultar respostas';
    }

    else if(button.classList.contains('btn-secondary')) {
        button.classList.remove('btn-secondary');
        button.classList.add('btn-primary');
        button.innerHTML = 'Mostrar respostas';
    }

});