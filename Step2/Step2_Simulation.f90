program step2_plant_intelligence
    implicit none
    integer, parameter :: fs = 10
    real, parameter :: tau = 10.0
    real, parameter :: threshold = 0.8
    real, parameter :: c_gain = 0.5
    real, parameter :: dt = 1.0 / real(fs)
    real, parameter :: T_sim = 60.0
    integer, parameter :: n_steps = int(T_sim * fs)
    
    real, dimension(0:n_steps) :: V_internal, u
    integer :: i
    real :: max_V_a, max_V_b
    logical :: act_a, act_b
    
    ! --- Case A: Single Stimulus ---
    V_internal = 0.0; u = 0.0
    u(int(5.0 * fs)) = c_gain
    
    act_a = .false.
    do i = 1, n_steps
        V_internal(i) = V_internal(i-1) + (-V_internal(i-1)/tau + u(i)) * dt
        if (V_internal(i) > threshold) act_a = .true.
    end do
    max_V_a = maxval(V_internal)
    
    ! --- Case B: Double Stimuli ---
    V_internal = 0.0; u = 0.0
    u(int(5.0 * fs)) = c_gain
    u(int(12.0 * fs)) = c_gain
    
    act_b = .false.
    do i = 1, n_steps
        V_internal(i) = V_internal(i-1) + (-V_internal(i-1)/tau + u(i)) * dt
        if (V_internal(i) > threshold) act_b = .true.
    end do
    max_V_b = maxval(V_internal)
    
    ! --- JSON Output ---
    open(10, file='Step2/simulation_results_fortran.json', status='replace')
    write(10, '(A)') '{'
    write(10, '(A)') '    "single_stimulus": {'
    if (act_a) then
        write(10, '(A)') '        "action_triggered": true,'
    else
        write(10, '(A)') '        "action_triggered": false,'
    end if
    write(10, '(A,F7.4)') '        "max_potential": ', max_V_a
    write(10, '(A)') '    },'
    write(10, '(A)') '    "double_stimuli": {'
    if (act_b) then
        write(10, '(A)') '        "action_triggered": true,'
    else
        write(10, '(A)') '        "action_triggered": false,'
    end if
    write(10, '(A,F7.4)') '        "max_potential": ', max_V_b
    write(10, '(A)') '    }'
    write(10, '(A)') '}'
    close(10)
    
end program step2_plant_intelligence
