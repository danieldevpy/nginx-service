import { Box, SimpleGrid, Stat, StatLabel, StatNumber, StatHelpText} from "@chakra-ui/react";
import { CardButton } from "./CardButton";
import { AddIcon } from "@chakra-ui/icons";
import { useModal } from "../contexts/ModalContext";
import { useServerRepository } from "../contexts/ServerRepositoryContext";
import CardStatusNginx from "./CardStatus";
import ReloadNginxOption from "./options/ReloadNginxOption";


export default function PanelNginx() {
  const { showModal } = useModal();
  const { servers } = useServerRepository();

  return (
    <Box>
      {/* Top Stats */}
      <SimpleGrid columns={{ base: 1, md: 4 }} spacing={6} mb={6}>
        <CardStatusNginx/>
        <Stat bg="white" p={4} borderRadius="md" shadow="md">
          <StatLabel>Total Servidores</StatLabel>
          <StatNumber>{servers.length}</StatNumber>
          <StatHelpText>👥</StatHelpText>
        </Stat>
        <Stat bg="white" p={4} borderRadius="md" shadow="md">
          {/* <StatLabel>Revenue</StatLabel>
          <StatNumber>$12,396</StatNumber>
          <StatHelpText>🛒</StatHelpText> */}
        </Stat>
         <Stat bg="white" p={4} borderRadius="md" shadow="md">
          {/* <StatLabel>Revenue</StatLabel>
          <StatNumber>$12,396</StatNumber>
          <StatHelpText>🛒</StatHelpText> */}
        </Stat>
     
      </SimpleGrid>

      <SimpleGrid columns={{ base: 1, md: 4 }} spacing={6} mb={6}>
        <CardButton
          label='Registrar Servidor'
          icon={AddIcon}
          onClick={()=>showModal("create-server")}/>
          <ReloadNginxOption/>
      </SimpleGrid>

    </Box>
  );
}
