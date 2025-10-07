import { useGlobalComponents } from '../contexts/GlobalComponents';
import { useModal } from '../contexts/ModalContext'
import { ServerFormProvider } from '../contexts/ServerFormContext'
import { useServerRepository } from '../contexts/ServerRepositoryContext';
import type { Server } from '../models/Server';
import type { ResponseError } from '../services/ServerAPI';
import formatFastAPI422Error from '../utils/fastpiError';
import ServerForm from './ServerForm';

export default function CreateServerFromModal() {
    const { onClose } = useModal();
    const { createServer } = useServerRepository();
    const { showMessage, showBackDrop } = useGlobalComponents();

    const createServerHandle = (server: Server) => {
        showBackDrop(true);
        createServer(server)
        .then(server => {
            showMessage({
                title: 'Servidor criado!',
                description: server.serverName,
                status: "success"
            })
            onClose();
        })
        .catch((response: ResponseError)=>{
            let err;
            if (response.statusCode == 422) {
                err = formatFastAPI422Error(response.error);
            }
            showMessage({
                title: 'Erro ao tentar criar server!',
                description: err? err : response.error.message,
                status: "warning"
            })
        })
        .finally(()=> showBackDrop(false));
    }

    return (
        <ServerFormProvider>
            <ServerForm label='Registrar' onSubmit={createServerHandle}/>
        </ServerFormProvider>
    )
}