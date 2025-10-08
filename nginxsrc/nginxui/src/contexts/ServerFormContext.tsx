import React from "react";
import { useForm, type UseFormReturn } from "react-hook-form";
import type { Server } from "../models/Server";

interface ServerFormType {
  form: UseFormReturn<Server>;
}

interface ServerFormProps {
  initialValue?: Server;
  children: React.ReactNode;
}

const ServerFormContext = React.createContext<ServerFormType | null>(null);

function ServerFormProvider({ initialValue, children }: ServerFormProps) {
  const defaultServer: Server = initialValue ?? {
    serverName: "",
    locations: [],
    ssl: {
      active: false,
    },
    extraSettings: [],
  };

  const form = useForm<Server>({
    defaultValues: defaultServer,
  });

  React.useEffect(() => {
    console.log("Form values:", form.getValues());
  }, [form]);

  return (
    <ServerFormContext.Provider value={{ form }}>
      {children}
    </ServerFormContext.Provider>
  );
}

const useServerForm = () => {
  const context = React.useContext(ServerFormContext);
  if (!context) throw new Error("useServerForm must be used inside ServerFormProvider");
  return context;
};

export { ServerFormProvider, useServerForm };
