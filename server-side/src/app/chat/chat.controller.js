export default class ChatService {
    constructor() {
    }

    async chat(req, res) {
        res.render('chat', { title: 'Chat de Soporte' });
    }
}