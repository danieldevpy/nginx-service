import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
} from '@chakra-ui/react'
import { useServerForm } from '../../contexts/ServerFormContext'

interface AccordionProps {
    children: any;
}

export default function AccordionSettings({children}: AccordionProps) {
    const { form } = useServerForm();
    const { extraSettings } = form.watch();

    return (
        <Accordion allowToggle>
            <AccordionItem>
                <h2>
                <AccordionButton>
                    <Box as='span' flex='1' textAlign='left'>
                        Configurações {`(${ extraSettings.length})`}                    
                    </Box>
                    <AccordionIcon />
                </AccordionButton>
                </h2>
                <AccordionPanel pb={4}>
                    {children}
                </AccordionPanel>
            </AccordionItem>
        </Accordion>
    )
}