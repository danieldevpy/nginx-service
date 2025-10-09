import React from "react";
import type { Server } from "../models/Server";
import { GetAllServers, CreateServer, DeleteServer, EditServer } from "../services/ServerAPI";
import SSLApi from "../services/SSLApi";

interface ServerRepositoryType {
    servers: Server[];
    createServer: (server: Server) => Promise<Server>;
    editServer: (server: Server) => Promise<Server>;
    deleteServer: (id: number) => Promise<void>;
    getServerById: (id: number) => Server | undefined;
    installSSL: (id: number) => Promise<Server>;
};

interface ServerRepositoryProps {
    children: any;
};

const ServerRepositoryContext = React.createContext<ServerRepositoryType | null>(null);

function ServerRepositoryProvider({children}: ServerRepositoryProps) {
    const [servers, setServers] = React.useState<Server[]>([]);

    const getAllServers = () => {
        GetAllServers()
        .then(servers => setServers(servers))
        .catch(error => console.log(error));
    }

    const getServerById = (id: number) => servers.find(s=>s.id === id);

    const createServer = (server: Server): Promise<Server> => {
        return new Promise(async(resolve, reject)=>{
            try {
                const serverCreated = await CreateServer(server);
                setServers(prev => [...prev, serverCreated]);
                resolve(serverCreated);
            } catch (response) {
                reject(response);
            }
        })
    }


    const editServer = (server: Server): Promise<Server> => {
        return new Promise(async (resolve, reject) => {
            try {
                const serverEdit = await EditServer(server);
                setServers(prev =>
                    prev.map(s => (s.id === serverEdit.id ? serverEdit : s))
                );
                resolve(serverEdit);
                } catch (response) {
                reject(response);
                }
        });
    };

    const deleteServer = async(id: number) => {
        try {
            await DeleteServer(id);
            setServers(prev => prev.filter(s=> s.id !== id));
        }
        catch (response) {
            throw response;
        }
    };

    const installSSL = async(id: number): Promise<Server> => {
        const api = new SSLApi();
        return new Promise(async(resolve, reject)=>{
            try {
                const server = await api.install(id, "danielfernandes202@gmail.com");
                setServers(prev =>
                    prev.map(s => (s.id === server.id ? server : s))
                );
                resolve(server);
            }
            catch (responseError) {
                return reject(responseError)
            }
        })
    }

    React.useEffect(()=>{
        getAllServers();
    }, [])

    return (
        <ServerRepositoryContext.Provider value={{
            servers,
            createServer,
            deleteServer,
            getServerById,
            editServer,
            installSSL
        }}>
            {children}
        </ServerRepositoryContext.Provider>
    )
}

function useServerRepository() {
    const context = React.useContext(ServerRepositoryContext);
    if (!context) throw new Error("useServerRepository deve ser usado dentro de ServerRepositoryProvider");
    return context;
}
export {
    useServerRepository,
    ServerRepositoryProvider
};