import { Navigate } from "react-router-dom"
import { jwtDecode } from "jwt-decode"
import api from "../api"
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants"
import { useEffect, useState } from "react"
import { ReactNode } from "react";

function ProtectedRoute({ children }: { children: ReactNode }) {
    const [isAuthorizer, setIsAuthorized] = useState<boolean | null>(null)
    
    useEffect(() => {
        const auth = async () => {
            const token = localStorage.getItem(ACCESS_TOKEN)
            if (!token) {
                setIsAuthorized(false)
                return
            }
            const decoded = jwtDecode(token)
            const tokenExpiration = decoded.exp
            const now = Date.now() / 1000

            if (tokenExpiration && tokenExpiration < now) {
                await refreshToken()
            } else {
                setIsAuthorized(true)
            }
        }

        auth().catch(() => setIsAuthorized(false))
    }, [])

    const refreshToken = async () => {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN)
        try {
            const response = await api.post('/api/token/refresh/', {refresh: refreshToken})
            if (response.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, response.data.access)
                setIsAuthorized(true)
            } else {
                setIsAuthorized(false)
            }
        } catch (error) {
            console.error(error)
            setIsAuthorized(false)
        }
    }

    if (isAuthorizer === null) {
        return <div>Loading...</div>
    }

    return isAuthorizer ? children : <Navigate to="/login" />
}

export default ProtectedRoute