import React from "react";
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
} from '@chakra-ui/react'

// Tipos
interface ModalType {
  registerComponent: (key: string, component: ModalComponent) => void;
  showModal: (key: string) => void;
  onClose: () => void;
  isSelected: (key: string) => boolean;
}

interface ModalComponent {
  key: string;
  title: string;
  element: React.ReactNode;
}

interface ModalProps {
  initComponents?: ModalComponent[];
  children: React.ReactNode;
}

const ModalContext = React.createContext<ModalType | null>(null);

function ModalProvider({ initComponents, children }: ModalProps) {
  const [selectedComponent, setSelectedComponent] = React.useState<ModalComponent>();
  const componentsRef = React.useRef<Record<string, ModalComponent>>({}); // Armazena os componentes

  const { isOpen, onOpen, onClose } = useDisclosure();

  const registerComponent = (key: string, component: ModalComponent) => {
    componentsRef.current[key] = component;
  }

  const showModal = (key: string) => {
    const comp = componentsRef.current[key];
    if (!comp) {
      console.warn(`Componente não encontrado para a chave: ${key}`);
      return;
    }
    setSelectedComponent(comp);
    onOpen();
  }

  const isSelected = (key: string) => selectedComponent?.title === key;

  React.useEffect(()=>{
    if(!initComponents) return;
    initComponents.forEach(node=>registerComponent(node.key, node));
  }, []);

  return (
    <ModalContext.Provider value={{ registerComponent, showModal, onClose, isSelected }}>
      {children}
      <Modal isOpen={isOpen} onClose={onClose} size={{ base: "full", md: "xl" }}>
        <ModalOverlay />
        <ModalContent
            w={{ base: "100%", md: "80%", lg: "50%"  }}
            h={{ base: "100%", md: "auto" }}
            maxH={{ base: "100%", md: "80vh" }} // no desktop, altura máxima 80% da tela
          >
          <ModalHeader>{selectedComponent?.title}</ModalHeader>
          <ModalCloseButton />
          <ModalBody overflow="auto">
            {selectedComponent?.element}
          </ModalBody>
        </ModalContent>
      </Modal>
    </ModalContext.Provider>
  )
}

function useModal() {
  const context = React.useContext(ModalContext);
  if (!context) throw new Error("useModal deve ser usado dentro de ModalProvider");
  return context;
}

export {
  ModalProvider,
  useModal,
  type ModalComponent
};
