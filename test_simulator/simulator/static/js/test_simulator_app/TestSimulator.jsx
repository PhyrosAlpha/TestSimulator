const QUESTIONS_CSS = {
    height:"400px", overflow:"scroll"}

const TestSimulator = ({test_id, test_size}) => {

    const [ questions, setQuestions ] = React.useState([]);
    const [ target, setTarget ] = React.useState(0);
    const testData = React.useRef({});
    const modalController = React.useRef();
    const [ loading, setLoading ] = React.useState(false);
    const [ activedTimer, setActivedTimer ] = React.useState(true);
    const [ percent, setPercent ] = React.useState(0);

    React.useEffect( () => {
        async function fetchData() {
            try {
                const LINK = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/simulator/test/start/${test_id}?size=${test_size}`
                const response = await fetch(LINK);
                const data = await response.json();
                
                testData.current = new TestData(data.test_id, data.questions, false);

                let result = data.questions;
                setQuestions(result);
                setLoading(false);
            } catch(error) {
                setLoading(false);
            }
        }
        setLoading(true);
        fetchData();
    }, [])

    function isAnswerSheet() {
        return target >= questions.length && questions.length > 0
    }

    function handleNext() {
        renderTestPercent()
        if(questions.length > target + 1){
            setTarget(target + 1);
        }
    }

    function handlePrevious() {
        renderTestPercent()
        if(target > 0){
            setTarget(target - 1);
        }
    }

    function handleGoAnswerSheet() {
        renderTestPercent()
        setTarget(questions.length);
    }

    function handleJumpToQuestion(index) {
        renderTestPercent()
        setTarget(index);
    }

    function handleSend() {
        if(isAnswerSheet()) {
            if(!testData.current.checkIfAllQuestionsAreAnswered()){
                modalController.current.showModal('Ops!', 'Nem todas as questões foram respondidas tem certeza que quer enviar mesmo assim?', sendTest);
            }else {
                modalController.current.showModal('Ops!', 'Deseja realmente enviar?', sendTest);
            }
        }else {
            modalController.current.showModal('Ops!', 'Verifique o gabarito antes de enviar.', null);
            handleGoAnswerSheet();
        }
    }

    function sendTest() {

        async function sendTest() {
            const LINK = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/simulator/test/correct`;
            const response = await fetch(LINK, {method: "POST", headers: {
                "Content-Type": "application/json"}, body:JSON.stringify(testData.current)});
            const data = await response.json();
            console.log(data);
            testData.current = new TestData(data.question_id, data.questions, true);
            testData.current.setPontuation(data.corrects, data.incorrects);
            modalController.current.closeModal();
            setActivedTimer(false);
            setLoading(false);
        }
        setLoading(true)
        sendTest();

    }

    function renderBody() {
        
        if(isAnswerSheet()) {
            return <AnswerSheet testData={testData.current} handleJumpToQuestion={handleJumpToQuestion} />
        }
        if(target >= 0 && target < questions.length) {
            let question = questions[target];
            return (<Question 
                        key={target} 
                        questionIndex={target}
                        testData={testData.current}
                        text={question.question_text} 
                        options={question.options} />)
        }
    }

    function renderTestPercent() {
        if(Object.keys(testData.current).length > 0 && testData.current.corrected === false ){
            setPercent(testData.current.getTestPercent());
        }
    }

    return (
        <div>
            {loading ? 
                <div className="d-flex justify-content-center">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
                :
                <div>
                    <div>
                        {/*<i className="bi bi-bar-chart-steps"></i>*/}
                        {percent}%
                        <div className="progress mb-2" role="progressbar" aria-label="Basic example" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
                            <div className="progress-bar progress-bar-striped" style={{width:`${percent}%`}}></div>
                        </div>
                    </div>
                    <Timer minutes={1} active={activedTimer} timeIsOverEvent={() => {
                        console.log("UHUUU disparou");
                        //handleGoAnswerSheet();
                        //sendTest();
                    }}/>
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
                        <button className="btn btn-success" disabled={testData.current.corrected}  onClick={handleSend}>Enviar</button>
                    </div>

                    <Modal modalController={modalController} />
                </div>
            }
        </div>
    );
}

class TestData {
    test_id = null;
    questions = [];
    corrected = false;
    corrects = 0;
    incorrects = 0;

    constructor(test_id, questions, corrected) {
        this.test_id = test_id;
        if(!corrected){
            this._buildQuestions(questions);
        }else {
            this.questions = questions;
        }
        this.corrected = corrected;
    }

    _buildQuestions(questions) {
        questions.forEach((question, index) => {
            this.questions.push({
                question_id: question.id,
                answers: []
            })
        })
    }

    setPontuation(corrects, incorrects) {
        this.corrects = corrects;
        this.incorrects = incorrects;
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

    getTestPercent() {
        let totalQuestions = this.questions.length;
        let totalRepliedQuestions = 0;
        for(let question of this.questions) {
            if(question.answers.length > 0){
                totalRepliedQuestions += 1;
            }
        }
        let result = (totalRepliedQuestions * 100) / totalQuestions;
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
const test_size = document.getElementById('test-size').value;
const rootNode = document.getElementById('root');
const root = ReactDOM.createRoot(rootNode);
root.render(React.createElement(TestSimulator, {test_id: test_id, test_size: test_size}));