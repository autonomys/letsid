import { NextResponse } from 'next/server'
import { verifyAutoID } from '../../../utils/verifyAutoId'

export const GET = async () => {
    if (await verifyAutoID()) return NextResponse.json({
        message: 'Hello Internet Identity Workshop! \n Nuclear code acquired! \n A.I. Agent booting...'
    })
    else return NextResponse.json({
        message: 'Access unauthorized!'
    })
}