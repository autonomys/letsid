type LetsIDResponse = {
    auto_id: string
    exists: boolean
    expired_at: string
    issuer: string
    sn: number
    start_at: string
    subject: string
    valid: boolean
}

export const verifyAutoID = async () => {
    if (!process.env.LETSID_ENDPOINT || !process.env.AUTO_ID) return false

    const check = await fetch(`${process.env.LETSID_ENDPOINT}verify/${process.env.AUTO_ID}`).then((response) => response.json()) as LetsIDResponse

    if (check.exists && check.valid && check.auto_id === process.env.AUTO_ID) return true

    return false
}