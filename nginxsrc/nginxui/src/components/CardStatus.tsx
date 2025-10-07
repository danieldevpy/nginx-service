import { Stat, StatLabel, StatNumber } from "@chakra-ui/react";
import { useSettingsNginx } from "../contexts/SettingsNginxContext";
import React from "react";


export default function CardStatusNginx(){
    const { getStatus } = useSettingsNginx();
    const [status, setStatus] = React.useState("");

    React.useEffect(()=>{
        getStatus().then((text)=>setStatus(text));
    }, []);

    return (
         <Stat bg="white" p={4} borderRadius="md" shadow="md">
            <StatLabel>Status Servidor</StatLabel>
            <StatNumber>{status}</StatNumber>
            {/* <StatHelpText>👥</StatHelpText> */}
        </Stat>
    )
}