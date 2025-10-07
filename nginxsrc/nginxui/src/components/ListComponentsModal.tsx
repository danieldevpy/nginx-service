import { type ModalComponent } from "../contexts/ModalContext"
import CreateServerFromModal from "./CrateServerFromModal";
import EditServerFromModal from "./EditServerFromModal";

const ComponentsFromModal: ModalComponent[] = [
    {key: "create-server", title: "Registrar Servidor", element: <CreateServerFromModal/>},
    {key: "edit-server", title: "Modificar Servidor", element: <EditServerFromModal/>}
]

export default ComponentsFromModal;