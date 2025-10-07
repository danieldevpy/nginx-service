import React from "react";
import { useServerForm } from "../../contexts/ServerFormContext";
import {
  Checkbox,
  FormControl,
  Box,
} from "@chakra-ui/react";

export default function SSLField() {
    const { form } = useServerForm();
    const [isChecked, setIsChecked] = React.useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setIsChecked(e.target.checked);
    };


    return (
        <Box>
          <Checkbox isChecked={isChecked} onChange={handleChange}>
            Usar SSL
          </Checkbox>
        </Box>
    );
}
