import React from "react";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  createColumnHelper,
  getPaginationRowModel,
} from "@tanstack/react-table";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Checkbox,
  Badge,
  HStack,
  Box,
  Button,
  ButtonGroup,
  Text,
  Select,
  Flex,
  useBreakpointValue,
} from "@chakra-ui/react";
import { useServerRepository } from "../contexts/ServerRepositoryContext";
import { useServerOptions } from "../contexts/ServerOptionsContext";
import type { Server } from "../models/Server";
import { differenceInDays, differenceInHours, isPast } from "date-fns";

export default function TableServers() {
  const { servers } = useServerRepository();
  const { setSelectedIds } = useServerOptions();
  const [rowSelection, setRowSelection] = React.useState({});

  // Configurações responsivas
  const tableVariant = useBreakpointValue({ base: "simple", md: "striped" });
  const isMobile = useBreakpointValue({ base: true, md: false });

  const columnHelper = createColumnHelper<Server>();

  const columns = [
    columnHelper.display({
      id: "select",
      header: ({ table }) => {
        const isAllSelected = table.getIsAllRowsSelected();
        const isSomeSelected = table.getIsSomeRowsSelected();
        
        return (
          <Flex alignItems="center" justifyContent="center">
            <Checkbox
              isChecked={isAllSelected}
              isIndeterminate={isSomeSelected}
              onChange={table.getToggleAllRowsSelectedHandler()}
              colorScheme="blue"
              size={isMobile ? "md" : "lg"}
              sx={{
                "& .chakra-checkbox__control": {
                  borderRadius: "4px",
                  borderWidth: "2px",
                  borderColor: isAllSelected ? "blue.500" : "gray.300",
                  bg: isAllSelected ? "blue.500" : "white",
                  _hover: {
                    borderColor: "blue.400",
                    bg: isAllSelected ? "blue.600" : "gray.50",
                  },
                  "&[data-indeterminate]": {
                    bg: "blue.500",
                    borderColor: "blue.500",
                  },
                },
              }}
            />
          </Flex>
        );
      },
      cell: ({ row }) => (
        <Flex alignItems="center" justifyContent="center">
          <Checkbox
            isChecked={row.getIsSelected()}
            isIndeterminate={row.getIsSomeSelected()}
            onChange={row.getToggleSelectedHandler()}
            colorScheme="blue"
            size={isMobile ? "md" : "lg"}
            sx={{
              "& .chakra-checkbox__control": {
                borderRadius: "4px",
                borderWidth: "2px",
                borderColor: row.getIsSelected() ? "blue.500" : "gray.300",
                bg: row.getIsSelected() ? "blue.500" : "white",
                _hover: {
                  borderColor: "blue.400",
                  bg: row.getIsSelected() ? "blue.600" : "gray.50",
                },
              },
            }}
          />
        </Flex>
      ),
      size: isMobile ? 40 : 60,
      minSize: 40,
    }),
    columnHelper.accessor("id", {
      header: "ID",
      size: isMobile ? 50 : 80,
      minSize: 50,
    }),
    columnHelper.accessor("serverName", {
      header: "Server Name",
      size: isMobile ? 120 : 200,
      minSize: 100,
    }),
    columnHelper.accessor("locations", {
      header: "Locations",
      size: isMobile ? 200 : 400,
      minSize: 150,
      cell: (info) => (
        <HStack spacing={1} wrap={isMobile ? "wrap" : "nowrap"}>
          {info.getValue().map((loc: any, i: number) => (
            <Badge
              key={i}
              colorScheme={loc.type === "proxy" ? "green" : "blue"}
              fontSize={isMobile ? "xs" : "sm"}
              maxW={isMobile ? "120px" : "none"}
              isTruncated
            >
              {isMobile 
                ? `${loc.type}: ${loc.path}`
                : `${loc.type} from '${loc.path}' to '${loc.proxyPass}'`
              }
            </Badge>
          ))}
        </HStack>
      ),
    }),
    columnHelper.accessor("listen", {
      header: "Listen",
      size: isMobile ? 70 : 100,
      minSize: 60,
    }),
columnHelper.accessor("ssl", {
    header: "SSL",
    size: 80,
    cell: (ssl) => {
      if (!ssl) return "—";

      // const { active, expiry } = ssl;
      const active = ssl.getValue().active;
      const expiry = ssl.getValue().expiry;
      const expiryDate = expiry ? new Date(expiry) : null;

      // Caso tenha data de expiração
      if (expiryDate) {
        if (isPast(expiryDate)) {
          return <span style={{ color: "red" }}>Expirado</span>;
        }

        if (active) {
          const diffDays = differenceInDays(expiryDate, new Date());
          const diffHours = differenceInHours(expiryDate, new Date());
          const timeLeft =
            diffDays > 0
              ? `${diffDays} dia${diffDays > 1 ? "s" : ""} restantes`
              : `${diffHours} hora${diffHours > 1 ? "s" : ""} restantes`;

          return (
            <span style={{ color: "green" }}>
              Ativo ({timeLeft})
            </span>
          );
        }

        return (
          <span style={{ color: "orange" }}>
            Não instalado (expira em{" "}
            {expiryDate.toLocaleDateString("pt-BR", {
              day: "2-digit",
              month: "2-digit",
              year: "numeric",
            })
            })
          </span>
        );
      }

      // Se não tiver data de expiração
      return active ? (
        <span style={{ color: "green" }}>Ativo</span>
      ) : (
        <span style={{ color: "gray" }}>Não instalado</span>
      );
    },
  }),
  ];

  const table = useReactTable({
    data: servers,
    columns,
    state: { 
      rowSelection,
    },
    enableRowSelection: true,
    onRowSelectionChange: setRowSelection,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getRowId: (originalRow, index) => originalRow.id? originalRow.id.toString() : index.toString(),
    initialState: {
      pagination: {
        pageSize: 10,
      },
    },
    // Habilita auto-resize
    defaultColumn: {
      minSize: 40,
    },
  });

  React.useEffect(() => {
    const selectedIds = Object.keys(rowSelection).map((id) => Number(id));
    setSelectedIds(selectedIds);
  }, [rowSelection, setSelectedIds]);

  return (
    <Box
      overflow="auto"
      maxWidth="100%"
      position="relative"
      css={{
        "&::-webkit-scrollbar": {
          height: "8px",
          width: "8px",
        },
        "&::-webkit-scrollbar-track": {
          background: "gray.100",
        },
        "&::-webkit-scrollbar-thumb": {
          background: "gray.400",
          borderRadius: "4px",
        },
        "&::-webkit-scrollbar-thumb:hover": {
          background: "gray.500",
        },
      }}
    >
      {/* Tabela */}
      <Table 
        variant={tableVariant}
        size={isMobile ? "sm" : "md"}
        minWidth="600px" // Largura mínima antes do scroll horizontal
      >
        <Thead>
          {table.getHeaderGroups().map((hg) => (
            <Tr key={hg.id}>
              {hg.headers.map((header) => (
                <Th
                  key={header.id}
                  width={`${header.column.columnDef.size || 150}px`}
                  minWidth={`${header.column.columnDef.minSize || 60}px`}
                  px={isMobile ? 2 : 4}
                  py={3}
                  fontSize={isMobile ? "xs" : "sm"}
                  whiteSpace="nowrap"
                >
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </Th>
              ))}
            </Tr>
          ))}
        </Thead>
        <Tbody>
          {table.getRowModel().rows.map((row) => (
            <Tr 
              key={row.id}
              bg={row.getIsSelected() ? "blue.50" : "transparent"}
              _hover={{
                bg: row.getIsSelected() ? "blue.100" : "gray.50",
              }}
            >
              {row.getVisibleCells().map((cell) => (
                <Td
                  key={cell.id}
                  width={`${cell.column.columnDef.size || 150}px`}
                  minWidth={`${cell.column.columnDef.minSize || 60}px`}
                  px={isMobile ? 2 : 4}
                  py={3}
                  fontSize={isMobile ? "xs" : "sm"}
                >
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </Td>
              ))}
            </Tr>
          ))}
        </Tbody>
      </Table>

      {/* Controles de Paginação - Responsivos */}
      <Flex
        justifyContent="space-between"
        alignItems={isMobile ? "flex-start" : "center"}
        mt={4}
        px={2}
        gap={4}
        direction={isMobile ? "column" : "row"}
      >
        <Text fontSize="sm" color="gray.600" mb={isMobile ? 2 : 0}>
          {table.getFilteredSelectedRowModel().rows.length} de{" "}
          {table.getFilteredRowModel().rows.length} linha(s) selecionada(s) •{" "}
          Página {table.getState().pagination.pageIndex + 1} de{" "}
          {table.getPageCount()}
        </Text>

        <Flex 
          alignItems="center" 
          gap={4} 
          flexWrap="wrap"
          justifyContent={isMobile ? "space-between" : "flex-end"}
          width={isMobile ? "100%" : "auto"}
        >
          <Flex alignItems="center" gap={2}>
            <Text fontSize="sm" whiteSpace="nowrap">
              Itens por página:
            </Text>
            <Select
              size="sm"
              value={table.getState().pagination.pageSize}
              onChange={(e) => {
                table.setPageSize(Number(e.target.value));
              }}
              w="auto"
              minW="80px"
            >
              {[5, 10, 20, 30, 40, 50].map((pageSize) => (
                <option key={pageSize} value={pageSize}>
                  {pageSize}
                </option>
              ))}
            </Select>
          </Flex>

          <ButtonGroup 
            size="sm" 
            isAttached 
            variant="outline"
            flexWrap={isMobile ? "wrap" : "nowrap"}
          >
            <Button
              onClick={() => table.firstPage()}
              isDisabled={!table.getCanPreviousPage()}
            >
              {isMobile ? "⏮" : "Primeira"}
            </Button>
            <Button
              onClick={() => table.previousPage()}
              isDisabled={!table.getCanPreviousPage()}
            >
              {isMobile ? "◀" : "Anterior"}
            </Button>
            <Button
              onClick={() => table.nextPage()}
              isDisabled={!table.getCanNextPage()}
            >
              {isMobile ? "▶" : "Próxima"}
            </Button>
            <Button
              onClick={() => table.lastPage()}
              isDisabled={!table.getCanNextPage()}
            >
              {isMobile ? "⏭" : "Última"}
            </Button>
          </ButtonGroup>
        </Flex>
      </Flex>
    </Box>
  );
}