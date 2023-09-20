const Toast = ({ message, toastController }) => {

    const toastElement = React.useRef();

    React.useEffect(() => {
        toastController.current = new bootstrap.Toast(toastElement.current);
    }, []);
        

    return (
        <div className="position-fixed bottom-0 end-0 p-3" style={{zIndex:'11'}}>
            <div className="toast" role="alert" aria-live="assertive" aria-atomic="true" ref={toastElement} >
                <div className="toast-body">
                    {message}
                    <div class="mt-2 pt-2 border-top">
                        <button type="button" className="btn btn-primary btn-sm me-2">Ok</button>
                        <button type="button" className="btn btn-secondary btn-sm" data-bs-dismiss="toast">Close</button>
                    </div>
                </div>
            </div>
        </div>
    )
}

const Modal = ({modalController}) => {

    const modalElement = React.useRef();
    const [modalInfo, setModalInfo] = React.useState({title:"", message:"", action:() => {}});

    React.useEffect(() => {
        const initModal = new bootstrap.Modal(modalElement.current);
        modalController.current = {
            showModal:(title, message, action= () => {}) =>  {
                setModalInfo({title:title, message:message, action:action});
                initModal.show();
            }
        }
    }, []);

    return (
        <div className="modal fade" data-bs-backdrop="static" tabIndex="-1" ref={modalElement}>
            <div className="modal-dialog">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">{modalInfo.title}</h5>
                        <button type="button" className="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div className="modal-body">
                        {modalInfo.message}
                    </div>
                    <div className="modal-footer">
                        {   modalInfo.action != null ?
                            <>
                                <button className="btn btn-success" onClick={modalInfo.action}>Confirmar</button>
                                <button className="btn btn-danger" data-bs-dismiss="modal">Cancelar</button>
                            </> 
                            :
                            <button className="btn btn-success" data-bs-dismiss="modal">Ok</button>
                        }
                    </div>
                </div>
            </div>
        </div>
    )

}

