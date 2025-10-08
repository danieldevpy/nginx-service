import {
  VStack,
  HStack,
  FormControl,
  FormLabel,
  Input,
  Select,
  Button,
} from "@chakra-ui/react";
import { useServerForm } from "../../contexts/ServerFormContext";
import React from "react";

// Lista de configurações disponíveis por padrão
const DEFAULT_SETTINGS = [
  { key: "client_max_body_size", placeholder: "Ex: 40M" },
  { key: "client_body_timeout", placeholder: "Ex: 60s" },
  { key: "keepalive_timeout", placeholder: "Ex: 75s" },
  { key: "send_timeout", placeholder: "Ex: 30s" },
  { key: "expires", placeholder: "Ex: 7d" },
  { key: "gzip", placeholder: "Ex: on" },
  { key: "add_header", placeholder: 'Ex: "X-Frame-Options SAMEORIGIN"' },
];


export default function ExtraSettingsField() {
  const { form } = useServerForm();

  const {extraSettings} = form.watch();

  const addSetting = (key: string, value: string) => {
    form.setValue("extraSettings", [...extraSettings, `${key} ${value}`]);
  };

  const removeSetting = (index: number) => {
    form.setValue(
      "extraSettings",
      extraSettings.filter((_, i) => i !== index)
    );
  };

  return (
    <VStack align="start" spacing={4} w="100%">
       {extraSettings.map((line, i) => (
        <HStack key={i} w="100%" spacing={4}>
          <Input value={line} isReadOnly bg="gray.50" />
          <Button colorScheme="red" onClick={() => removeSetting(i)}>
            Remover
          </Button>
        </HStack>
      ))}
      <DynamicSettingSelector onAdd={addSetting} />
    </VStack>
  );
}

function DynamicSettingSelector({
  onAdd,
}: {
  onAdd: (key: string, value: string) => void;
}) {
  const [selectedKey, setSelectedKey] = React.useState("");
  const [customValue, setCustomValue] = React.useState("");

  const selectedSetting = DEFAULT_SETTINGS.find((s) => s.key === selectedKey);

  return (
    <HStack spacing={4} w="100%">
      <FormControl>
        <FormLabel>Opção</FormLabel>
        <Select
          placeholder="Selecione uma configuração"
          value={selectedKey}
          onChange={(e) => setSelectedKey(e.target.value)}
        >
          {DEFAULT_SETTINGS.map((s) => (
            <option key={s.key} value={s.key}>
              {s.key}
            </option>
          ))}
        </Select>
      </FormControl>

      <FormControl>
        <FormLabel>Valor</FormLabel>
        <Input
          placeholder={selectedSetting?.placeholder ?? "Valor"}
          value={customValue}
          onChange={(e) => setCustomValue(e.target.value)}
        />
      </FormControl>

      <Button
        mt={6}
        colorScheme="blue"
        onClick={() => {
          onAdd(selectedKey, customValue);
          setSelectedKey("");
          setCustomValue("");
        }}
        isDisabled={!selectedKey || !customValue}
      >
        Adicionar
      </Button>
    </HStack>
  );
}
