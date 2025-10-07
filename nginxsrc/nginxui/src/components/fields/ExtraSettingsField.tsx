import { useServerForm } from "../../contexts/ServerFormContext";
import {
  Textarea,
  FormControl,
  FormLabel,
} from "@chakra-ui/react";

export default function ExtraSettingsField() {
    const { form } = useServerForm();

    return (
        <FormControl>
          <FormLabel>Configurações Extras</FormLabel>
          <Textarea
            placeholder="Digite linhas extras"
            {...form.register("extraSettings.lines")}
          />
        </FormControl>
    );
}
