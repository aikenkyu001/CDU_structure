program step1_cdu_electronics
    implicit none
    integer, parameter :: fs = 100
    real, parameter :: tau = 3.2
    real, parameter :: V_threshold = 0.6
    real, parameter :: V_pulse = 0.5
    real, parameter :: dt = 1.0 / real(fs)
    
    real, dimension(:), allocatable :: t, Vmem, u
    integer :: i, n_steps, interval_idx
    real :: interval_sec, T_sim, max_V_ok, max_V_ng
    logical :: success_ok, success_ng
    
    ! --- Case A: 2.0s Interval ---
    interval_sec = 2.0
    T_sim = max(interval_sec + 2.0, 6.0)
    n_steps = int(T_sim * fs)
    allocate(t(0:n_steps), Vmem(0:n_steps), u(0:n_steps))
    
    t = 0.0; Vmem = 0.0; u = 0.0
    u(int(0.5 * fs)) = V_pulse
    u(int((0.5 + interval_sec) * fs)) = V_pulse
    
    success_ok = .false.
    do i = 1, n_steps
        t(i) = real(i) * dt
        Vmem(i) = Vmem(i-1) + (-Vmem(i-1)/tau + u(i)) * dt
        if (Vmem(i) > V_threshold) success_ok = .true.
    end do
    max_V_ok = maxval(Vmem)
    deallocate(t, Vmem, u)
    
    ! --- Case B: 5.0s Interval ---
    interval_sec = 5.0
    T_sim = max(interval_sec + 2.0, 6.0)
    n_steps = int(T_sim * fs)
    allocate(t(0:n_steps), Vmem(0:n_steps), u(0:n_steps))
    
    t = 0.0; Vmem = 0.0; u = 0.0
    u(int(0.5 * fs)) = V_pulse
    u(int((0.5 + interval_sec) * fs)) = V_pulse
    
    success_ng = .false.
    do i = 1, n_steps
        t(i) = real(i) * dt
        Vmem(i) = Vmem(i-1) + (-Vmem(i-1)/tau + u(i)) * dt
        if (Vmem(i) > V_threshold) success_ng = .true.
    end do
    max_V_ng = maxval(Vmem)
    
    ! --- JSON Output ---
    open(10, file='Step1/simulation_results_fortran.json', status='replace')
    write(10, '(A)') '{'
    write(10, '(A)') '    "success_case": {'
    write(10, '(A,F5.2,A)') '        "interval": 2.00,'
    if (success_ok) then
        write(10, '(A)') '        "success": true,'
    else
        write(10, '(A)') '        "success": false,'
    end if
    write(10, '(A,F7.4)') '        "max_voltage": ', max_V_ok
    write(10, '(A)') '    },'
    write(10, '(A)') '    "failed_case": {'
    write(10, '(A,F5.2,A)') '        "interval": 5.00,'
    if (success_ng) then
        write(10, '(A)') '        "success": true,'
    else
        write(10, '(A)') '        "success": false,'
    end if
    write(10, '(A,F7.4)') '        "max_voltage": ', max_V_ng
    write(10, '(A)') '    }'
    write(10, '(A)') '}'
    close(10)
    
    deallocate(t, Vmem, u)
    
end program step1_cdu_electronics
