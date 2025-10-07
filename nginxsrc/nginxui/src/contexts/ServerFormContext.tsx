import React from "react";
import { useForm, type UseFormReturn } from "react-hook-form";
import type { Server } from "../models/Server";

interface ServerFormType {
    form: UseFormReturn<Server>;
}

interface ServerFormProps {
    initialValue?: Server;
    children: any;
}

const ServerFormContext = React.createContext<ServerFormType | null>(null);

function ServerFormProvider({initialValue, children}: ServerFormProps) {
    const defaultServer = initialValue ? initialValue : {
        serverName: "",
    }
    const form = useForm<Server>({defaultValues: defaultServer})
    console.log(form.getValues());
    return (
        <ServerFormContext.Provider value={{form}}>
            {children}
        </ServerFormContext.Provider>
    )
}

const useServerForm = () => {
    const context = React.useContext(ServerFormContext);
    if (!context) throw new Error("...");
    return context;
}

export {
    ServerFormProvider,
    useServerForm
}