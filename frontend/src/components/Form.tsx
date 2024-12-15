import { useState } from "react"
import api from "../api"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"
import { useNavigate } from "react-router-dom"
import '../styles/Form.css'

interface FormProps {
    route: string;
    method: 'Login' | 'Register';
}

function Form({ route, method }: FormProps) {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const handleSubmit = async (e: { preventDefault: () => void }) => {
        setLoading(true)
        e.preventDefault()
        setLoading(true)
        try {
            const response = await api.post(route, {email, password})
            if(method === 'Login' && response.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, response.data.access)
                localStorage.setItem(REFRESH_TOKEN, response.data.refresh)
                navigate('/')
            } else if (method === 'Register' && response.status === 200) {
                navigate('/login')
            }
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{method}</h1>
                <input className="form-input" type="text" value={email} placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
                <input className="form-input" type="password" value={password} placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
            <button className="form-button" type="submit" disabled={loading}>{method}</button>
        </form>
    )
}

export default Form