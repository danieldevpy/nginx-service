import React from "react";

interface ServerOptionsType {
    selectedIds: number[];
    setSelectedIds: React.Dispatch<React.SetStateAction<number[]>>;
    removeSelection: (id: number) => void;
}

interface ServerOptionsProps {
    children: any;
}

const ServerOptionsContext = React.createContext<ServerOptionsType | null>(null);

function ServerOptionsProvider({children}: ServerOptionsProps) {
    const [selectedIds, setSelectedIds] = React.useState<number[]>([]);

    const removeSelection = (id: number) => {
        setSelectedIds(selectedIds.filter((selectedId) => selectedId !== id));
    }

    return (
        <ServerOptionsContext.Provider value={{
            selectedIds,
            setSelectedIds,
            removeSelection
        }}>
            {children}
        </ServerOptionsContext.Provider>
    );
};

const useServerOptions = () => {
  const ctx = React.useContext(ServerOptionsContext);
  if (!ctx) {
    throw new Error("useServerOptions must be used inside ServerOptionsContext");
  }
  return ctx;
};

export {
    ServerOptionsProvider,
    useServerOptions
}

