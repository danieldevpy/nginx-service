import { Box } from "@chakra-ui/react";
import FloatingBar from "./FloatingBar";
import ActionButton from "./ActionButton";
import { EditIcon, DeleteIcon } from "@chakra-ui/icons"
import { useServerOptions } from "../contexts/ServerOptionsContext";
import { useServerRepository } from "../contexts/ServerRepositoryContext";
import { useGlobalComponents } from "../contexts/GlobalComponents";
import { useModal } from "../contexts/ModalContext";


export default function SelectedOptions() {
    const { selectedIds, removeSelection } = useServerOptions();
    const { deleteServer , getServerById} = useServerRepository();
    const { showMessage, showBackDrop, showConfirmation } = useGlobalComponents();
    const { showModal } = useModal();

    const deleteServerHandle = () => {
        selectedIds.forEach(id=>{
            console.log(id);
            const server = getServerById(id);
            showConfirmation({
                title: `Deseja realmente apagar ${server?.serverName}?`,
                handleConfirm() {
                    showBackDrop(true);
                    deleteServer(id)
                    .then(()=>{
                        removeSelection(id);
                        showMessage({
                            title: "Servidor Removido",
                            description: server?.serverName,
                            status: "success"
                        })
                    })
                    .finally(()=> showBackDrop(false));
                },
            })
        })  
    }

    const count = selectedIds.length;

    return (
        <Box>
            {count > 0 &&(
             <FloatingBar> 
                    {count === 1 && (
                        <>
                         <ActionButton
                            title="EDITAR"
                            icon={<EditIcon/>}
                            colorScheme="teal"
                            onClick={()=> showModal("edit-server")}/>
                        </>
                    )}
                    <ActionButton
                        title={`DELETAR ${count > 1? "TODOS": ""}`}
                        icon={<DeleteIcon/>}
                        colorScheme="red"   // sobrescreve o padrão teal
                        onClick={deleteServerHandle}/>
                </FloatingBar>
            )}
        </Box>
    );
}