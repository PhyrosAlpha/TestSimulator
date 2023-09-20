const ANSWER_SHEET = {};
const LETTER = ["A", "B", "C", "D", "E"];
const AnswerSheet = ({testData, handleJumpToQuestion}) => {

    function renderAnswer(answers, index) {
        let ANSWER_SHEET_ANSWER = {padding:"2px 4px", color:"white", backgroundColor:"#0d6efd", cursor:"pointer", borderRadius:"5px"};

        let answerSTR = "";
        if(answers.length > 0) {
            answers.forEach((answer, index) => {
                answerSTR += LETTER[answer.option_index];
                if(index < answers.length - 1) {
                    answerSTR += ", ";
                }
            });
        }else {
            ANSWER_SHEET_ANSWER['backgroundColor'] = "#dc3545";
            answerSTR = "Sem resposta";
        }
        
        return <p style={ANSWER_SHEET_ANSWER} 
                        onClick={() => {handleJumpToQuestion(index)}} 
                        className="ms-2" key={index}>
                            {index + 1} - {answerSTR}
                        </p>
    }

    return(
        <div>
            <h3>Gabarito</h3>
            <div style={{display:"flex", flexWrap:"wrap"}}>
                {testData.questions.map((question, index) => {
                    return renderAnswer(question.answers, index);
                })}
            </div>
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
        {option_id: option_id, option_index: index}));

    function handleOptionClick() {
        testData.setQuestionAnswerByIndex(questionIndex, {option_id: option_id, option_index: index});
        setMarked(!marked);
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