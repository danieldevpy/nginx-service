import { useGlobalComponents } from "../contexts/GlobalComponents";
import { useServerOptions } from "../contexts/ServerOptionsContext";
import { useServerRepository } from "../contexts/ServerRepositoryContext";
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Button,
} from "@chakra-ui/react";
import { ChevronDownIcon, RepeatIcon, UnlockIcon, DeleteIcon } from "@chakra-ui/icons";


export default function SslOptionsMenu() {
    const { selectedIds } = useServerOptions();
    const {  getServerById, installSSL } = useServerRepository();
    // const { showModal } = useModal();
    const {showBackDrop, showMessage} = useGlobalComponents();
    const serverSelected = getServerById(selectedIds[0]);

    const install = async() => {
        const idSelected = selectedIds[0];
        if (!idSelected) return ;
        showBackDrop(true);
        try {
            const server = await installSSL(idSelected);
            showMessage({
                title: "Certificado SSL instalado!",
                description: server.serverName,
                status: "success"
            })
        }
        catch (response: any) {
            let err;
            if (response.statusCode == 422) {
                // @ts-ignore
                err = formatFastAPI422Error(response.error);
            }
            showMessage({
                title: "Erro ao instalar SSL",
                description: err? err : response.error.message,
                duration: 10000,
            status: "warning"
            })
        }
        finally {
            showBackDrop(false);
        }
    }
    
    return (
        <Menu placement="top">
        <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
            Opções de SSL
        </MenuButton>
            {selectedIds.length === 1 && serverSelected &&(
                <MenuList>
                    {serverSelected.ssl.active? (
                        <>
                            <MenuItem icon={<RepeatIcon />} onClick={install}>
                                Reinstalar SSL
                            </MenuItem>
                            <MenuItem icon={<DeleteIcon />} onClick={install} color="red.500">
                                Remover SSL
                            </MenuItem>
                        </>
                    ): (
                        <MenuItem icon={<UnlockIcon />} onClick={install}>
                            Instalar SSL
                        </MenuItem>
                    )}
                </MenuList>
            )}
        </Menu>
  );
}


