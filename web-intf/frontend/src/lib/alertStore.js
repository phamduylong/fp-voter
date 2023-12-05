import { writable } from 'svelte/store';

const initialState = {
    message: '',
    type: '',
    visible: false
};


function createAlert(){
    const { subscribe, set } = writable(initialState);
    return {
        subscribe,
        show: (msg, alertType) => set({message:msg, type:alertType, visible:true}),
        hide: () => set({message: "", type: "", visible:false}),
    }
}

const alertState = createAlert();
export { alertState };