import React from "react";
import {
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Box,
  Spinner,
  Flex,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  useDisclosure,
} from "@chakra-ui/react";

interface GlobalComponentsContextProps {
  showBackDrop: (visible: boolean) => void;
  showMessage: (options: {
    status?: "success" | "error" | "warning" | "info";
    title?: string;
    description?: string;
    duration?: number;
  }) => void;
  showConfirmation: (options: {
    title: string;
    handleConfirm: () => void;
  }) => void;
}

const GlobalComponentsContext = React.createContext<GlobalComponentsContextProps | undefined>(undefined);

export const GlobalComponentsProvider = ({ children }: { children: React.ReactNode }) => {
  const [backdropVisible, setBackdropVisible] = React.useState(false);
  const [message, setMessage] = React.useState<{
    status: "success" | "error" | "warning" | "info";
    title?: string;
    description?: string;
  } | null>(null);
  const [messageVisible, setMessageVisible] = React.useState(false);

  // Confirm modal state
  const [confirmOptions, setConfirmOptions] = React.useState<{
    title: string;
    handleConfirm: () => void;
  } | null>(null);
  const { isOpen, onOpen, onClose } = useDisclosure();

  const showBackDrop = (visible: boolean) => setBackdropVisible(visible);

  const showMessage = ({
    status = "info",
    title,
    description,
    duration = 3000,
  }: {
    status?: "success" | "error" | "warning" | "info";
    title?: string;
    description?: string;
    duration?: number;
  }) => {
    setMessage({ status, title, description });
    setMessageVisible(true);
    setTimeout(() => setMessageVisible(false), duration);
  };

  const showConfirmation = ({
    title,
    handleConfirm,
  }: {
    title: string;
    handleConfirm: () => void;
  }) => {
    setConfirmOptions({ title, handleConfirm });
    onOpen();
  };

  const handleConfirmClick = () => {
    if (confirmOptions) confirmOptions.handleConfirm();
    onClose();
    setConfirmOptions(null);
  };

  const handleCancelClick = () => {
    onClose();
    setConfirmOptions(null);
  };

  return (
    <GlobalComponentsContext.Provider value={{ showBackDrop, showMessage, showConfirmation }}>
      {children}

      {/* Backdrop */}
      {backdropVisible && (
        <Flex
          position="fixed"
          top={0}
          left={0}
          w="100vw"
          h="100vh"
          bg="blackAlpha.600"
          align="center"
          justify="center"
          zIndex={1400}
        >
          <Spinner size="xl" color="white" />
        </Flex>
      )}

      {/* Alert */}
      {messageVisible && message && (
        <Box position="fixed" top={4} right={4} zIndex={1500} maxW="sm">
          <Alert status={message.status} borderRadius="md" boxShadow="lg">
            <AlertIcon />
            <Box>
              {message.title && <AlertTitle>{message.title}</AlertTitle>}
              {message.description && (
                <AlertDescription fontSize={14}>{message.description}</AlertDescription>
              )}
            </Box>
          </Alert>
        </Box>
      )}

      {/* Confirmation Modal */}
      <Modal isOpen={isOpen} onClose={handleCancelClick} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{confirmOptions?.title}</ModalHeader>
          <ModalBody>
            Deseja realmente prosseguir com esta ação?
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={handleCancelClick}>
              Cancelar
            </Button>
            <Button colorScheme="red" onClick={handleConfirmClick}>
              Confirmar
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </GlobalComponentsContext.Provider>
  );
};

export const useGlobalComponents = () => {
  const ctx = React.useContext(GlobalComponentsContext);
  if (!ctx) {
    throw new Error("useGlobalComponents must be used inside GlobalComponentsProvider");
  }
  return ctx;
};
