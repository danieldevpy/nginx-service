import DashboardFake from './components/NginxPanel';
import SelectedOptions from './components/SelectedOptions';
import TableServers from './components/TableServers';
import { CONTENT_WIDTHS } from './utils/settingsGeral';
import { Tabs, TabList, TabPanels, Tab, TabPanel, Flex } from "@chakra-ui/react";

function App() {
  return (
    <Flex justifyContent={"center"}>
      <Flex 
        w={CONTENT_WIDTHS}
        direction={"column"}
        gap={5}
        >
        <Tabs variant="enclosed" colorScheme="teal">
          <TabList>
            <Tab>Principal</Tab>
            <Tab>Logs</Tab>
          </TabList>

          <TabPanels>
            {/* principal */}
            <TabPanel
              display={"flex"}
              flexDirection="column"
              gap={5}>
              <DashboardFake/>
              <TableServers/>
            </TabPanel>
            </TabPanels>
        </Tabs>

        <SelectedOptions/>
      </Flex>
    </Flex>
  )
}

export default App
