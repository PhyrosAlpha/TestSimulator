//import { print, test} from './test_import.js';
//relative('')

console.log("Iniciado start_simulator.js")
// print();
// console.log(test);

// questions = [];
// screens = [];
// currentScreen = 0;

// //Iniciar eventos das opções.
// let options = document.querySelectorAll('.option');
// options.forEach(function(option) {
//     option.addEventListener('click', handleOption);
// });

// //Iniciar Objetos das questões
// let questions_html = document.querySelectorAll('.question');
// questions_html.forEach(function(question) {
//     screens.push(question);

//     questions.push({
//         id:question.attributes.getNamedItem("id"),
//         answers:[]
//     });
// });

// //Iniciar eventos dos botões
// let previousButton = document.querySelector('#previous-button');
// previousButton.addEventListener('click', handlePreviousQuestion);

// let nextButton = document.querySelector('#next-button');
// nextButton.addEventListener('click', handleNextQuestion);

// function handleOption(event){
//     let index = event.target.attributes.getNamedItem("index").value;
//     let optionIndex = event.target.attributes.getNamedItem("option-index").value;
//     let questionIndex = event.target.attributes.getNamedItem("question-index").value;
//     console.log("index: " + index + " Questão: " + questionIndex + " Opção: " + optionIndex);
//     let selectedQuestion = questions[index];
//     updateAnswer(selectedQuestion.answers, optionIndex);
//     console.log(questions);
// }

// function updateAnswer(list, answer){
//     list.indexOf(answer) === -1 ? 
//     list.push(answer) : 
//     list.splice(list.indexOf(answer), 1);
// }

// function handleNextQuestion(event){
//     console.log("Next question");
//     if(currentScreen < screens.length-1){
//         screens[currentScreen].classList.remove("show-question");
//         screens[currentScreen+1].classList.add("show-question");
//         currentScreen++;
//     }
// }

// function handlePreviousQuestion(event){
//     console.log("Previous question");
//     if(currentScreen > 0){
//         screens[currentScreen].classList.remove("show-question");
//         screens[currentScreen-1].classList.add("show-question");
//         currentScreen--;
//     }
// }

//window.onload = function() {

    // class HelloClass extends React.Component 
    // {
    //     render() {
    //         return React.createElement("div", null, "React without npm");
    //     }
    // }

    // ReactDOM.render(
    //     React.createElement(Component, null, null),
    //     document.getElementById("root")
    // );    

//}