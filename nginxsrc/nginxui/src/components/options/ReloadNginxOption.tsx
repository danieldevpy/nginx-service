import { RepeatIcon } from "@chakra-ui/icons"
import { CardButton } from "../CardButton"
import { useSettingsNginx } from "../../contexts/SettingsNginxContext"
import { useGlobalComponents } from "../../contexts/GlobalComponents";


export default function ReloadNginxOption() {
    const { reload } = useSettingsNginx();
    const { showMessage } = useGlobalComponents();

    const handleReload = () => {
        reload()
        .then(()=>{
            showMessage({
                title: "Settings Nginx",
                description: "O nginx foi reniciado!",
                status: "success"
            })
        })
        .catch(() => {
            showMessage({
                title: "Settings Nginx",
                description: "Erro ao tentar reiniciar nginx",
                status: "error"
            })
        })
    }

    return (
        <CardButton
          label='Reiniciar Nginx'
          icon={RepeatIcon}
          onClick={handleReload}/>
    )
}