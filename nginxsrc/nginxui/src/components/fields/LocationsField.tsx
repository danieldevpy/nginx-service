import { useServerForm } from "../../contexts/ServerFormContext";
import {
  FormControl,
  FormLabel,
  Input,
  Select,
  Button,
  VStack,
  HStack,
  Checkbox,
} from "@chakra-ui/react";
import { useFieldArray, useWatch } from "react-hook-form";
import { LocationTypeEnum } from "../../models/Location";

export default function LocationsField() {
  const { form } = useServerForm();

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "locations",
  });

  // Observe todos os tipos de locations
  const watchLocations = useWatch({
    control: form.control,
    name: "locations",
  }) as any[];

  return (
    <VStack align="start" spacing={4}>
      {fields.map((field, index) => {
        const type = watchLocations?.[index]?.type;

        return (
          <VStack key={field.id} p={4} borderWidth={1} borderRadius="md" spacing={4} align="start">
            <HStack spacing={4} w="100%">
              <FormControl isRequired>
                <FormLabel>Path</FormLabel>
                <Input
                  placeholder="/exemplo"
                  {...form.register(`locations.${index}.path` as const, { required: "Path obrigatório" })}
                />
              </FormControl>

              <FormControl isRequired>
                <FormLabel>Tipo</FormLabel>
                <Select
                  {...form.register(`locations.${index}.type` as const, { required: "Tipo obrigatório" })}
                >
                  {Object.values(LocationTypeEnum).map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </Select>
              </FormControl>

              <Button colorScheme="red" mt={6} onClick={() => remove(index)}>
                Remover
              </Button>
            </HStack>

            {/* Render inputs específicos dependendo do type */}
            {type === "proxy" && (
              <FormControl isRequired>
                <FormLabel>Proxy Pass</FormLabel>
                <Input
                  placeholder="https://example.com"
                  {...form.register(`locations.${index}.proxyPass` as const, {
                    required: "Proxy Pass obrigatório",
                  })}
                />
              </FormControl>
            )}

            {type === "redirect" && (
              <FormControl isRequired>
                <FormLabel>Redirect To</FormLabel>
                <Input
                  placeholder="https://example.com/redirect"
                  {...form.register(`locations.${index}.redirectTo` as const, {
                    required: "Redirect To obrigatório",
                  })}
                />
                
                <FormLabel>Status Code</FormLabel>
                <Input
                  type="number"
                  defaultValue={301}
                  placeholder="301"
                  {...form.register(`locations.${index}.status_code` as const, {
                    required: "Redirect To obrigatório",
                  })}
                />
                
              </FormControl>
            )}

            {type === "static" && (
              <FormControl isRequired>
                <FormLabel>Root</FormLabel>
                <Input
                  placeholder="/var/www/html"
                  {...form.register(`locations.${index}.root` as const, {
                    required: "Root obrigatório",
                  })}
                />
              </FormControl>
            )}

            {type === "rewrite" && (
              <FormControl isRequired>
                <FormLabel>Rewrite Rule</FormLabel>
                <Input
                  placeholder="rewrite ^/old /new;"
                  {...form.register(`locations.${index}.rewriteRule` as const, {
                    required: "Rewrite Rule obrigatório",
                  })}
                />
              </FormControl>
            )}

            {type === "maintenance" && (
              <FormControl>
                <Checkbox {...form.register(`locations.${index}.last` as const)}>
                  Última Location
                </Checkbox>
              </FormControl>
            )}
          </VStack>
        );
      })}

      <Button onClick={() => append({ path: "", type: "proxy" })} colorScheme="blue">
        Adicionar Location
      </Button>
    </VStack>
  );
}
