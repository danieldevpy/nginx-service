import { useServerForm } from "../../contexts/ServerFormContext";
import {
  Input,
  FormControl,
  FormLabel,
  FormErrorMessage,
} from "@chakra-ui/react";

export default function ServerNameField() {
    const { form } = useServerForm();
    const errors = form.formState.errors;

    return (
        <FormControl isInvalid={!!errors.serverName}>
          <FormLabel>Server Name</FormLabel>
          <Input
            placeholder="cisbaf.org.br"
            {...form.register("serverName", {
              required: "Server name obrigatório!",
              validate: (value) =>
                !/^https?:\/\//i.test(value) || "Não pode ser uma URL completa (http:// ou https://)",
            })}
          />
          <FormErrorMessage>
            {errors.serverName && errors.serverName.message}
          </FormErrorMessage>
        </FormControl>
    );
}