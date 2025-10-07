import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { ModalProvider } from './contexts/ModalContext.tsx'
import { ServerRepositoryProvider } from './contexts/ServerRepositoryContext.tsx'
import { GlobalComponentsProvider } from './contexts/GlobalComponents.tsx'
import ComponentsFromModal from './components/ListComponentsModal.tsx'
import { ChakraProvider } from '@chakra-ui/react'
import { ServerOptionsProvider } from './contexts/ServerOptionsContext.tsx'
import { SettingsNginxProvider } from './contexts/SettingsNginxContext.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ChakraProvider>
      <GlobalComponentsProvider>
        <SettingsNginxProvider>
        <ServerRepositoryProvider>
          <ServerOptionsProvider>
            <ModalProvider initComponents={ComponentsFromModal}>
              <App />
            </ModalProvider>
          </ServerOptionsProvider>
        </ServerRepositoryProvider>
      </SettingsNginxProvider>
    </GlobalComponentsProvider>
    </ChakraProvider>
  </StrictMode>,
)
