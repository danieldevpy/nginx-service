import React from "react";
import {
  Box,
  Text,
  Flex,
  Icon,
  useColorModeValue,
  type BoxProps,
} from "@chakra-ui/react";

interface CardButtonProps extends BoxProps {
  label: string;
  icon?: React.ElementType;
  onClick?: () => void;
}

const CardButton: React.FC<CardButtonProps> = ({
  label,
  icon,
  onClick,
  ...rest
}) => {
  const bg = useColorModeValue("gray.100", "gray.700");
  const hoverBg = useColorModeValue("gray.200", "gray.600");

  return (
    <Box
      as="button"
      onClick={onClick}
      p={6}
      borderRadius="2xl"
      boxShadow="lg"
      bg={bg}
      _hover={{ bg: hoverBg, transform: "scale(1.05)" }}
      _active={{ transform: "scale(0.98)" }}
      transition="all 0.2s"
      w="200px"
      h="150px"
      {...rest} // 👈 permite sobrescrever/estender estilos
    >
      <Flex
        direction="column"
        align="center"
        justify="center"
        h="100%"
        gap={3}
      >
        {icon && <Icon as={icon} boxSize={10} color="teal.400" />}
        <Text fontSize="lg" fontWeight="bold">
          {label}
        </Text>
      </Flex>
    </Box>
  );
};

export { CardButton };
