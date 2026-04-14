program step2_data_analysis_fortran
    implicit none
    character(len=2048) :: line, part
    integer :: status, i, j, k, l, pipe_count
    real :: charge
    integer :: behavior_val
    real, dimension(100) :: unique_charges
    integer, dimension(100) :: trial_counts, success_counts
    integer :: n_unique = 0
    real :: critical_charge = -1.0
    
    unique_charges = 0.0; trial_counts = 0; success_counts = 0

    open(10, file='Step2/data_repo/observation_data', status='old', action='read')

    do
        read(10, '(A)', iostat=status) line
        if (status /= 0) exit
        
        if (line(1:1) == '|') then
            pipe_count = 0
            do i = 1, len_trim(line)
                if (line(i:i) == '|') then
                    pipe_count = pipe_count + 1
                    
                    if (pipe_count == 6) then
                        j = i + 1
                        do k = j, len_trim(line)
                            if (line(k:k) == '|') exit
                        end do
                        part = adjustl(line(j:k-1))
                        read(part, *, iostat=status) charge
                        
                        if (status == 0) then
                            j = k + 1
                            do l = j, len_trim(line)
                                if (line(l:l) == '|') exit
                            end do
                            part = line(j:l-1)
                            
                            behavior_val = 0
                            if (index(part, 'droop') > 0 .or. index(part, 'close') > 0) then
                                behavior_val = 1
                            end if
                            
                            do j = 1, n_unique
                                if (abs(unique_charges(j) - charge) < 1e-6) then
                                    trial_counts(j) = trial_counts(j) + 1
                                    success_counts(j) = success_counts(j) + behavior_val
                                    exit
                                end if
                            end do
                            if (j > n_unique) then
                                n_unique = n_unique + 1
                                unique_charges(n_unique) = charge
                                trial_counts(n_unique) = 1
                                success_counts(n_unique) = behavior_val
                            end if
                        end if
                        exit 
                    end if
                end if
            end do
        end if
    end do
    close(10)

    do j = 1, n_unique
        if (trial_counts(j) > 0) then
            if (real(success_counts(j))/real(trial_counts(j)) >= 0.5) then
                if (critical_charge < 0.0 .or. unique_charges(j) < critical_charge) then
                    critical_charge = unique_charges(j)
                end if
            end if
        end if
    end do

    open(20, file='Step2/plant_data_analysis_fortran.json', status='replace')
    write(20, '(A)') '{'
    write(20, '(A,F7.4,A)') '    "critical_charge_uC": ', critical_charge, ','
    write(20, '(A)') '    "analysis_summary": ['
    do j = 1, n_unique
        write(20, '(A)') '        {'
        write(20, '(A,F10.6,A)') '            "Charge (uC)": ', unique_charges(j), ','
        write(20, '(A,I4,A)')    '            "Trials": ', trial_counts(j), ','
        write(20, '(A,F7.4)')    '            "Success Rate": ', real(success_counts(j))/real(trial_counts(j))
        if (j < n_unique) then
            write(20, '(A)') '        },'
        else
            write(20, '(A)') '        }'
        end if
    end do
    write(20, '(A)') '    ]'
    write(20, '(A)') '}'
    close(20)

end program step2_data_analysis_fortran
