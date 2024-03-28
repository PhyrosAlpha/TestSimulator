const ANSWER_SHEET_RED= {padding:"2px 4px", color:"white", backgroundColor:"#dc3545", cursor:"pointer", borderRadius:"5px"};
const ANSWER_SHEET_BLUE = {padding:"2px 4px", color:"white", backgroundColor:"#0d6efd", cursor:"pointer", borderRadius:"5px"};
const ANSWER_SHEET_GREEN = {padding:"2px 4px", color:"white", backgroundColor:"green", cursor:"pointer", borderRadius:"5px"};
const LETTERS = ["A", "B", "C", "D", "E"];

const AnswerSheet = ({testData, handleJumpToQuestion}) => {

    function renderQuestions() {
        return (
            <div style={{display:"flex", flexWrap:"wrap"}}>
                    {testData.questions.map((question, index) => {
                        return renderAnswer(question, index);
                    })}
            </div>)
    }

    function renderAnswer(question, index) {
        if(!testData.corrected){
            return testStatus(question, index);
        }else {
            return correctedStatus(question, index);
        }      
    }

    function testStatus(question, index) {
        let ANSWER_SHEET_ANSWER = ANSWER_SHEET_BLUE;
        let answers = question.answers;
        let answerSTR = "";
        if(answers.length > 0) {
            answers.forEach((answer, index) => {
                if(answer.option_index !== undefined){
                answerSTR += LETTERS[answer.option_index];
                    if(index < answers.length - 1) {
                        answerSTR += ", ";
                    }
                }
            });
        }else {
            ANSWER_SHEET_ANSWER = ANSWER_SHEET_RED
            answerSTR = "Sem resposta";
        }

        return <p style={ANSWER_SHEET_ANSWER} 
        onClick={() => {handleJumpToQuestion(index)}} 
        className="ms-2" key={index}>
            {index + 1} - {answerSTR}
        </p>

    }

    function correctedStatus(question, index) {
        let ANSWER_SHEET_ANSWER = ANSWER_SHEET_BLUE;
        let answers = question.answers;
        let answerSTR = "";
        if(answers.length > 0) {
            answers.forEach((answer, index) => {
                if(answer.source === 'user'){
                answerSTR += LETTERS[answer.option_index];
                    if(index < answers.length - 1) {
                        answerSTR += ", ";
                    }
                }
            });
            answerSTR = answerSTR.substring(0, answerSTR.length);
            console.log(answerSTR)
        }else {
            ANSWER_SHEET_ANSWER = ANSWER_SHEET_RED
            answerSTR = "Sem resposta";
        }


        if(question.is_correct){
            ANSWER_SHEET_ANSWER = ANSWER_SHEET_GREEN;
        }else {
            ANSWER_SHEET_ANSWER = ANSWER_SHEET_RED;
        }
        
        return <p style={ANSWER_SHEET_ANSWER} 
        onClick={() => {handleJumpToQuestion(index)}} 
        className="ms-2" key={index}>
            {index + 1} - {answerSTR}
        </p>

    }

    //Mode Corrected
    function renderResult() {
        if (testData.corrected) {
            return (
                <div className="mb-4">
                    <div>Resultado:</div>
                    <span className="badge bg-success me-2">Corretas: {testData.corrects}</span>
                    <span className="badge bg-danger me-2">Incorretas: {testData.incorrects}</span>
                    <span className="badge bg-primary">Total: {testData.questions.length}</span>
                </div>)
        }
    }

    return(
        <div>
            <h3>Gabarito</h3>
            {renderResult()}
            {renderQuestions()}
        </div>
    )
}

const Question = ({text, options, questionIndex, testData}) => {
    return (
        <div>
            {getImg(questionIndex+1 + ' - ' + text)}
            <h6 className="mt-2">Alternativas:</h6>
            <ol type="A">
                {options.map((option, index) => <Option 
                                                    key={index} 
                                                    questionIndex={questionIndex} 
                                                    index={index} testData={testData} 
                                                    text={option.option_text} 
                                                    option_id={option.id} />
                            )}
            </ol>
        </div>
    )
}

const Option = ({text, questionIndex, index, testData, option_id}) => {   
    const [marked, setMarked] = React.useState(testData.optionIsMarked(
        questionIndex, 
        {option_id: option_id, option_index: index, by_user:true}));

    function handleOptionClick() {
        if(testData.corrected){
            return;

        }else {
            testData.setQuestionAnswerByIndex(questionIndex, {option_id: option_id, option_index: index, by_user:true});
            setMarked(!marked);
        }
    }

    return (
        <li style={{cursor:"pointer"}} className={marked ? "answer show-answer" : "answer"} onClick={handleOptionClick}>{getImg(text)}</li>
    )
}

function getImg(text){
    let index = text.indexOf("{img");
    if(index == -1){
        return <p className="card-text" style={{margin:"0"}}>{text}</p>;
    }

    let getted_img = "";
    let final = -1;
    let getted_href = "";
    while(true) {
        index = text.indexOf("{img");
        if(index == -1){
            return <p className="card-text" style={{margin:"0"}} dangerouslySetInnerHTML={{__html: text}}></p>;
        }
        getted_img = "";
        final = -1;
        let count = index;
        while(true){
            getted_img += text[count];
            if(text[count] == "}"){
                final = count;
                break;
            }
            count++;
        }
        getted_href = text.substring(index+4, final);
        text = text.replace(getted_img, '<img src="' + getted_href + '" style="max-width:100%;"><br>');
    }
}

const Timer = ({timeIsOverEvent, minutes, active}) => {

    const [now, setNow] = React.useState(new Date((minutes * 60 * 1000 + Date.now()) - Date.now()));
    const [percent, setPercent] = React.useState(0);
    const intervalId = React.useRef(null);

    React.useEffect( () => {
        let milesecondsTotal = minutes * 60 * 1000;
        let whenTimeIsOver = Date.now() + milesecondsTotal;
        
        if(active){
            let id = setInterval(() => {
                let time = whenTimeIsOver - Date.now();
                setNow(new Date(time));

                let result = (time * 100) / milesecondsTotal;
                setPercent(100-result);

                if(time <= 0) {
                    setNow(new Date(0));
                    timeIsOverEvent();
                    clearInterval(id);
                }
            }, 1000)
            intervalId.current = id;
        }

    }, [])

    React.useEffect(() => {
        if(!active){
            clearInterval(intervalId.current);
        }
    }, [active])

    function renderColor() {
        return percent <= 80 ? "bg-success" : "bg-danger"
    }

    function renderTime(){
        let minutes = now.getMinutes().toString().padStart(2, '0');
        let seconds = now.getSeconds().toString().padStart(2, '0');
        return `${minutes}:${seconds}`
    }

    return(
        <div>
            {renderTime()}
            <div className="progress mb-2" role="progressbar" aria-label="Basic example" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
                <div className={`progress-bar ${renderColor()}`}  style={{width:`${percent}%`}}></div>
            </div>
        </div>
    )
}