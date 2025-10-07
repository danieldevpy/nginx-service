import { useGlobalComponents } from '../contexts/GlobalComponents';
import { useModal } from '../contexts/ModalContext'
import { ServerFormProvider } from '../contexts/ServerFormContext'
import { useServerOptions } from '../contexts/ServerOptionsContext';
import { useServerRepository } from '../contexts/ServerRepositoryContext';
import type { Server } from '../models/Server';
import type { ResponseError } from '../services/ServerAPI';
import formatFastAPI422Error from '../utils/fastpiError';
import ServerForm from './ServerForm';


export default function EditServerFromModal() {
    const { onClose } = useModal();
    const { selectedIds } = useServerOptions();
    const { getServerById } = useServerRepository();
    const { editServer } = useServerRepository();
    const { showMessage, showBackDrop } = useGlobalComponents();

    const getSelected = () => {
        if (selectedIds.length !== 1) return undefined;
        return getServerById(selectedIds[0]);
    }

    const editServerHandle = (server: Server) => {
        showBackDrop(true);
        editServer(server)
        .then(server => {
            showMessage({
                title: 'Servidor modificado!',
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
                title: 'Erro ao tentar modificar server!',
                description: err? err : response.error.message,
                status: "warning"
            })
        })
        .finally(()=> showBackDrop(false));
    }

    return (
        <ServerFormProvider initialValue={getSelected()}>
            <ServerForm label='Salvar' onSubmit={editServerHandle}/>
        </ServerFormProvider>
    )
}