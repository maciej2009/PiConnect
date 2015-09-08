create table temperatury
            (
                data            datetime,
                temp_zew        dec(10,2),
                temp_co_zas     dec(10,2),
                temp_co_return  dec(10,2),
                temp_buf_top    dec(10,2),
                temp_buf_mid    dec(10,2),
                temp_buf_low    dec(10,2),
                temp_wew_01     dec(10,2),
                temp_wew_02     dec(10,2),
                temp_wew_03     dec(10,2),
                temp_wew_04     dec(10,2),
                temp_wew_05     dec(10,2),
                temp_wew_06     dec(10,2),
                temp_wew_07     dec(10,2),
                temp_wew_08     dec(10,2),
                temp_wew_09     dec(10,2),
                temp_wew_10     dec(10,2),
                temp_cwu        dec(10,2),
                temp_cwu_cyr    dec(10,2),

                CWU             int,
                CO              int,

                st_taryfa           int,
                st_co_pompa         int,
                st_cwu_pompa_cyr    int

            )
