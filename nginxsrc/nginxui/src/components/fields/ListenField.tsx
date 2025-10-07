import { useServerForm } from "../../contexts/ServerFormContext";
import {
  Input,
  FormControl,
  FormLabel,
  FormErrorMessage,
} from "@chakra-ui/react";

export default function ListenField() {
    const { form } = useServerForm();
    const errors = form.formState.errors;

    return (
        <FormControl isInvalid={!!errors.listen}>
          <FormLabel>Porta</FormLabel>
          <Input
            type="number"
            placeholder="Digite a porta"
            defaultValue={80}
            {...form.register("listen", { required: "Porta obrigatória!" })}
          />
          <FormErrorMessage>
            {errors.listen && errors.listen.message}
          </FormErrorMessage>
        </FormControl>
    );
}
