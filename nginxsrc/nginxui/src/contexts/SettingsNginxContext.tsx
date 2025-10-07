import React from "react";
import { SettingsReload, SettingsStatus } from "../services/SettingsAPI";

interface SettingsNginxType {
    reload: ()=> Promise<void>;
    getStatus: ()=> Promise<string>;
};

interface SettingsNginxProps {
    children: any;
};

const SettingsNginxContext = React.createContext<SettingsNginxType | null>(null);

function SettingsNginxProvider({children}: SettingsNginxProps) {

    const reload = ()=> SettingsReload();

    const getStatus = ()=> SettingsStatus();

    return (
        <SettingsNginxContext.Provider value={{
            reload,
            getStatus
        }}>
            {children}
        </SettingsNginxContext.Provider>
    )
}

const useSettingsNginx = () => {
  const ctx = React.useContext(SettingsNginxContext);
  if (!ctx) {
    throw new Error("useSettingsNginx must be used inside SettingsNginxContext");
  }
  return ctx;
};

export {
    SettingsNginxProvider,
    useSettingsNginx
}