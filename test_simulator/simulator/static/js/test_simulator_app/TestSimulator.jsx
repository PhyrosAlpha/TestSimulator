
const QUESTIONS_CSS = {
    height:"400px", overflow:"scroll"}

const TestSimulator = ({test_id}) => {

    const [ questions, setQuestions ] = React.useState([]);
    const [ target, setTarget ] = React.useState(0);
    const testData = React.useRef(new TestData());
    //const toastController = React.useRef();
    const modalController = React.useRef();

    React.useEffect( () => {
        async function fetchData() {
            //const response = await fetch(`${window.location.href}/simulator/test/start/` + test_id);
            const response = await fetch(`http://127.0.0.1:8000/simulator/test/start/` + test_id);
            const data = await response.json();
            testData.current.initTestData(data.test_id, data.questions);
            let result = data.questions.map((question, index) => <
            Question 
                key={index} 
                questionIndex={index}
                testData={testData.current}
                text={question.question_text} 
                options={question.options} />);
            setQuestions(result);
        }
        fetchData();
    }, [])

    function isAnswerSheet() {
        return target >= questions.length && questions.length > 0
    }

    function handleNext() {
        if(questions.length > target + 1){
            setTarget(target + 1);
        }
    }

    function handlePrevious() {
        if(target > 0){
            setTarget(target - 1);
        }
    }

    function handleGoAnswerSheet() {
        setTarget(questions.length);
    }

    function handleJumpToQuestion(index) {
        setTarget(index);
    }

    function handleSend() {
        if(isAnswerSheet()) {
            if(!testData.current.checkIfAllQuestionsAreAnswered()){
                modalController.current.showModal('Ops!', 'Nem todas as questões foram respondidas tem certeza que quer enviar mesmo assim?', sendTest);
                console.log(testData.current.getTestDataInJson())
            }else {
                modalController.current.showModal('Ops!', 'Deseja realmente enviar?', sendTest);
            }
        }else {
            modalController.current.showModal('Ops!', 'Verifique o gabarito antes de enviar.', null);
            handleGoAnswerSheet();
        }
    }

    function sendTest() {
        console.log("Enviando o teste!");

    }

    function renderBody() {
        
        if(isAnswerSheet()) {
            return <AnswerSheet testData={testData.current} handleJumpToQuestion={handleJumpToQuestion} />
        }
        if(target >= 0 && target < questions.length) {
            return questions[target]
        }
    }

    return (
        <div>
            <div className="card mb-2">
                <div className="card-body" style={QUESTIONS_CSS}>
                    {renderBody()}
                </div>
            </div>
            <div className="d-flex justify-content-end mt-2">
                <button className="btn btn-primary me-2" onClick={handlePrevious} disabled={target == 0}>Anterior</button>
                { target < questions.length - 1 ?
                    <button className="btn btn-primary me-2" onClick={handleNext} disabled={target + 1 >= questions.length}>Próxima</button>
                    :
                    null
                }
                <button className="btn btn-warning me-2" onClick={handleGoAnswerSheet}>Gabarito</button>
                <button className="btn btn-success" onClick={handleSend}>Enviar</button>
            </div>

            {/* <Toast message="Testando" toastController={toastController}/> */}
            <Modal modalController={modalController} />
        </div>
    );
}

class TestData {
    test_id = null;
    questions = [];

    constructor() {
        this.test_id = null;
        this.questions = [];
    }

    initTestData(test_id, questions) {
        this.test_id = test_id;
        this._buildQuestions(questions);
    }

    _buildQuestions(questions) {
        questions.forEach((question, index) => {
            this.questions.push({
                question_id: question.id,
                answers: []
            })
        })
    }

    setQuestionAnswerByIndex(index, currentAnswer) {
        let result = this.questions[index]
                                    .answers
                                        .findIndex((answer) => 
                                            answer.option_id == currentAnswer.option_id);

        if(result != -1) {
            this.questions[index].answers.splice(result, 1);
        }else {
            this.questions[index].answers.push(currentAnswer);
        }
    }

    getAnswersByIndex(index) {
        let result = this.questions[index].answers;
        return result;
    }

    optionIsMarked(index, currentAnswer) {
        let result = this.questions[index]
                                    .answers
                                        .find((answer) => 
                                            answer.option_id == currentAnswer.option_id);
        return result;
    }

    checkIfAllQuestionsAreAnswered() {
        let result = true;
        this.questions.forEach((question) => {
            if(question.answers.length == 0) {
                result = false;
            }
        });
        return result;
    }

    getTestDataInJson() {
        let result = {
            test_id: this.test_id,
            questions: this.questions
        }

        return JSON.stringify(result);
    }

}

const test_id = document.getElementById('test-id').value;
const rootNode = document.getElementById('root');
const root = ReactDOM.createRoot(rootNode);
root.render(React.createElement(TestSimulator, {test_id: test_id}));
