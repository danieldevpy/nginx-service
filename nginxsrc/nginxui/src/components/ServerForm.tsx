import { useServerForm } from "../contexts/ServerFormContext";
import ServerNameField from './fields/ServerName'
import ListenField from './fields/ListenField'
import SSLField from './fields/SLLField'
import LocationsField from './fields/LocationsField'
import { Button, Flex, Grid, GridItem } from "@chakra-ui/react";
import AccordionLocation from "./fields/AccordionLocation";
import type { Server } from "../models/Server";

interface ServerFormProps {
  label: string;
  onSubmit: (server: Server) => void;
}

export default function ServerForm({label, onSubmit}: ServerFormProps) {
    const { form } = useServerForm();

    const handleSubmit = form.handleSubmit(async (server) => onSubmit(server));

    return (
        <form
        onSubmit={handleSubmit}>
            <Flex
            direction="column"
            gap={10}>
                <Grid templateColumns="repeat(12, 1fr)" gap={4}>
                <GridItem colSpan={[12, 10]}><ServerNameField/></GridItem>
                <GridItem colSpan={[6, 2]}><ListenField/></GridItem>
                <GridItem colSpan={12}>
                    <AccordionLocation>
                    <LocationsField/>
                    </AccordionLocation>
                </GridItem>
                </Grid>
            <Button type="submit">{label}</Button>
            </Flex>
    </form>
  )
}