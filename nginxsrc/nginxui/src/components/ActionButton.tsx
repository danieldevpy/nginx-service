import { Button, Text, type ButtonProps } from "@chakra-ui/react";
import type React from "react";

interface ActionProps extends ButtonProps {
    title: string;
    icon: React.ReactElement;
}

export default function ActionButton({ title, icon, ...rest }: ActionProps) {
    return (
        <Button
            leftIcon={icon}
            borderRadius="md"
            _hover={{ transform: "translateY(-2px)", shadow: "md" }}
            _active={{ transform: "translateY(0px)", shadow: "sm" }}
            justifyContent={{ base: "center", md: "flex-start" }} // centraliza no mobile, ícone à esquerda em md+
            {...rest}
        >
            <Text
                fontWeight="bold"
                display={{ base: "none", md: "block" }} // esconde o texto no mobile
            >
                {title}
            </Text>
        </Button>
    );
}
