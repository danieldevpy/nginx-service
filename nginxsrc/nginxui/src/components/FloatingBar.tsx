import { Box, Flex } from "@chakra-ui/react"
import { motion } from "framer-motion"
import { CONTENT_WIDTHS } from "../utils/settingsGeral";

// Transformamos Box em um componente animável
const MotionBox = motion(Box)

interface FloatingBarProps {
    children: any;
}

export default function FloatingBar({children}: FloatingBarProps) {
    return (
        <Flex
            w={CONTENT_WIDTHS}
            position="fixed"
            bottom={10}
            justifyContent={"center"}>
            <MotionBox
                transform="translateX(-50%)"
                backgroundColor="#00000040"
                padding={6}
                borderRadius="md"
                // Animação inicial
                initial={{ y: 100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5, ease: "easeOut" }}
            >
                <Flex
                    wrap={"wrap"}
                    gap={5}>
                        {children}
                </Flex>
            </MotionBox>
        </Flex>
    )
}
