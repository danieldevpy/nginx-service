
import APIBACKEND from "./API";


export default class SSLApi extends APIBACKEND {

    constructor() {
        super("ssl"); // aqui você define o path
    }

    async install(id: number, email: string) {
        return this.response(
            fetch(this.urlBase, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ id, email })
            })
        )
    }
}