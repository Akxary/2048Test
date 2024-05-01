const BACK_URL = "http://localhost:8005";

export interface User {
    id:number;
    name: string;
    score:number;
}

export async function getUserByName(name: string): Promise<User> {
    return fetch(BACK_URL+ "/user/name/"+name).then(res => res.json()).then((res:User)=> res);
}

// const userName = 